import random

from sqlalchemy import func
from sqlalchemy.orm import Session

import for_how_much.models as models
from for_how_much.schemas import (
    AnswerInput,
    AnswerOutput,
    GetCategoriesOutput,
    GetQuestionOutput,
)


class QuestionService:
    def __init__(self, db: Session):
        self.db = db

    def get_categories(self) -> GetCategoriesOutput:
        """
        Get the categories.
        """
        categories = self.db.query(models.Question.category).distinct().all()
        return GetCategoriesOutput(categories=[category[0] for category in categories])

    def get_question(self, question_id: int) -> GetQuestionOutput:
        question = (
            self.db.query(
                models.Question.id,
                models.Question.text,
                models.Question.image_url,
                models.Question.type,
                models.Question.min_value,
                models.Question.max_value,
                models.Question.price_unit,
                models.Question.category,
                models.Stats.average_answer,
                models.Stats.number_of_answers,
            )
            .outerjoin(models.Stats)
            .filter(models.Question.id == question_id)
            .first()
        )
        return GetQuestionOutput(**question)

    def get_random_question(
        self, categories: list[str] | None = None
    ) -> GetQuestionOutput:
        if categories is None:
            random_offset = random.randint(
                0, self.db.query(func.count(models.Question.id)).scalar() - 1
            )

            question = (
                self.db.query(
                    models.Question.id,
                    models.Question.text,
                    models.Question.image_url,
                    models.Question.type,
                    models.Question.min_value,
                    models.Question.max_value,
                    models.Question.price_unit,
                    models.Question.category,
                    models.Stats.average_answer,
                    models.Stats.number_of_answers,
                )
                .outerjoin(models.Stats)
                .offset(random_offset)
                .limit(1)
                .first()
            )
        else:
            random_offset = random.randint(
                0,
                self.db.query(func.count(models.Question.id))
                .filter(models.Question.category.in_(categories))
                .scalar()
                - 1,
            )

            question = (
                self.db.query(
                    models.Question.id,
                    models.Question.text,
                    models.Question.image_url,
                    models.Question.type,
                    models.Question.min_value,
                    models.Question.max_value,
                    models.Question.price_unit,
                    models.Question.category,
                    models.Stats.average_answer,
                    models.Stats.number_of_answers,
                )
                .outerjoin(models.Stats)
                .filter(models.Question.category.in_(categories))
                .offset(random_offset)
                .limit(1)
                .first()
            )

        if question is None:
            return None

        return GetQuestionOutput(**question._asdict())

    def get_question_stats(self, question_id: int) -> AnswerOutput:
        stats = (
            self.db.query(models.Stats)
            .filter(models.Stats.question_id == question_id)
            .first()
        )
        return AnswerOutput(**stats)

    def submit_answer(self, answer: AnswerInput) -> AnswerOutput:
        stats = (
            self.db.query(models.Stats)
            .filter(models.Stats.question_id == answer.question_id)
            .first()
        )
        if stats is None:
            stats = models.Stats(
                question_id=answer.question_id,
                average_answer=answer.answer,
                number_of_answers=1,
            )
            self.db.add(stats)
        else:
            # Update average using the formula: average = average + (answer - average) / number_of_answers
            stats.average_answer = stats.average_answer + (
                answer.answer - stats.average_answer
            ) / (stats.number_of_answers + 1)
            stats.number_of_answers += 1

        self.db.commit()
        self.db.refresh(stats)

        return AnswerOutput(**stats)
