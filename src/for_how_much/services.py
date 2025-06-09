import logging
import random
import uuid

from sqlalchemy import func
from sqlalchemy.orm import Session

from for_how_much.models import Question, Stats, User
from for_how_much.schemas import (
    AnswerInput,
    AnswerOutput,
    GetCategoriesOutput,
    GetQuestionOutput,
    Token,
    UserDescription,
)

logger = logging.getLogger(__name__)


class QuestionService:
    def __init__(self, db: Session):
        self.db = db

    def get_categories(self) -> GetCategoriesOutput:
        """
        Get the categories.
        """
        categories = self.db.query(Question.category).distinct().all()
        return GetCategoriesOutput(categories=[category[0] for category in categories])

    def get_categories_questions(self, categories: list[str]) -> list[str]:
        questions = (
            self.db.query(Question.id).filter(Question.category.in_(categories)).all()
        )
        return [question[0] for question in questions]

    def get_question(self, question_id: int) -> GetQuestionOutput:
        question = (
            self.db.query(
                Question.id,
                Question.text,
                Question.image_url,
                Question.type,
                Question.min_value,
                Question.max_value,
                Question.price_unit,
                Question.category,
                Stats.average_answer,
                Stats.number_of_answers,
            )
            .outerjoin(Stats)
            .filter(Question.id == question_id)
            .first()
        )

        return GetQuestionOutput(**question._asdict())

    def get_random_question(
        self, categories: list[str] | None = None, user: UserDescription | None = None
    ) -> tuple[GetQuestionOutput, set[int]]:
        if categories is None:
            questions_pool = self.db.query(Question.id).all()
        else:
            questions_pool = (
                self.db.query(Question.id)
                .filter(Question.category.in_(categories))
                .all()
            )

        candidate_questions = set([question[0] for question in questions_pool])

        if user is not None:
            filtered_candidates = candidate_questions - set(user.answered_questions)
            if len(filtered_candidates) == 0:
                filtered_candidates = candidate_questions
                reset_questions = candidate_questions
            else:
                reset_questions = set()
        else:
            filtered_candidates = candidate_questions
            reset_questions = set()

        if len(filtered_candidates) == 0:
            raise ValueError("No questions found")

        question_id = random.choice(list(filtered_candidates))

        return self.get_question(question_id), reset_questions

    def get_question_stats(self, question_id: int) -> AnswerOutput:
        stats = self.db.query(Stats).filter(Stats.question_id == question_id).first()
        if stats is None:
            return AnswerOutput(average_answer=0, number_of_answers=0)
        return AnswerOutput(
            average_answer=stats.average_answer,
            number_of_answers=stats.number_of_answers,
        )

    def submit_answer(self, answer: AnswerInput) -> AnswerOutput:
        stats = (
            self.db.query(Stats).filter(Stats.question_id == answer.question_id).first()
        )
        if stats is None:
            stats = Stats(
                question_id=answer.question_id,
                average_answer=answer.answer,
                number_of_answers=1,
            )
        else:
            # Update average using the formula: average = average + (answer - average) / number_of_answers
            stats.average_answer = stats.average_answer + (
                answer.answer - stats.average_answer
            ) / (stats.number_of_answers + 1)
            stats.number_of_answers += 1

        self.db.add(stats)
        self.db.commit()
        self.db.refresh(stats)

        return self.get_question_stats(answer.question_id)


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def get_user_from_description(self, user_description: UserDescription) -> User:
        user = self.db.query(User).filter(User.id == user_description.id).first()
        if user is None:
            raise ValueError("User not found")
        return user

    def get_user_description(self, token: Token) -> UserDescription:
        user = self.db.query(User).filter(User.token == token.value).first()

        if user is None:
            return UserDescription()

        return UserDescription(
            id=user.id,
            number_of_seen_questions=user.number_of_seen_questions,
            answered_questions=user.answered_questions,
        )

    def get_all_users(self) -> list[UserDescription]:
        users = self.db.query(User).all()
        return [
            UserDescription(
                id=user.id,
                number_of_seen_questions=user.number_of_seen_questions,
                answered_questions=user.answered_questions,
                token=user.token,
            )
            for user in users
        ]

    def create_new_user(self) -> Token:
        token = str(uuid.uuid4())
        previous_max = self.db.query(func.max(User.id)).scalar()
        if previous_max is None:
            new_id = 1
        else:
            new_id = previous_max + 1
        user = User(
            id=new_id, token=token, number_of_seen_questions=0, answered_questions=[]
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return Token(value=token)

    def reset_user_answered_questions(
        self, reset_questions: set[int], user_description: UserDescription
    ) -> None:
        user = self.get_user_from_description(user_description)

        user.answered_questions = list(set(user.answered_questions) - reset_questions)
        self.db.commit()
        self.db.refresh(user)

    def answer_question(
        self, user_description: UserDescription, question_id: int
    ) -> None:
        user = self.get_user_from_description(user_description)

        user.number_of_seen_questions += 1
        if question_id not in user.answered_questions:
            user.answered_questions.append(question_id)
        else:
            logger.warning(
                f"Question {question_id} already answered by user {user_description.id}"
            )
        user.answered_questions = list(set(user.answered_questions))

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

    def get_user_answered_questions(
        self, user_description: UserDescription
    ) -> list[int]:
        user = self.get_user_from_description(user_description)
        return user.answered_questions
