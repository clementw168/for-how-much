from fastapi import Depends, FastAPI, HTTPException, Query, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

import for_how_much.database as database
import for_how_much.models as models
from for_how_much.database import get_db
from for_how_much.schemas import (
    AnswerInput,
    AnswerOutput,
    GetCategoriesOutput,
    GetQuestionOutput,
    MultiplayerResultsInput,
    MultiplayerResultsOutput,
    Token,
    UserDescription,
)
from for_how_much.services import QuestionService, UserService

# Create database tables if they don't exist
models.Base.metadata.create_all(bind=database.engine)

# Security scheme for Bearer token authentication
security = HTTPBearer()


def get_question_service(db=Depends(get_db)):
    return QuestionService(db=db)


def get_user_service(db=Depends(get_db)):
    return UserService(db=db)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(security),
    user_service: UserService = Depends(get_user_service),
) -> UserDescription:
    """
    Get the current user from the Bearer token.
    Raises HTTPException if token is invalid or user not found.
    """
    token = Token(value=credentials.credentials)
    user_description = user_service.get_user_description(token)
    if user_description.id is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user_description


app = FastAPI(
    title="For How Much API",
    description="API for the For How Much game",
    version="1.0.0",
)


@app.post("/user/new", response_model=Token)
def create_new_user(user_service: UserService = Depends(get_user_service)):
    return user_service.create_new_user()


@app.get("/users/all", response_model=list[UserDescription])
def get_all_users(user_service: UserService = Depends(get_user_service)):
    return user_service.get_all_users()


@app.get("/user/me", response_model=UserDescription)
def get_user_me(user_description: UserDescription = Depends(get_current_user)):
    return user_description


@app.post("/user/reset_questions")
def reset_user_answered_questions(
    reset_questions: list[int],
    user_service: UserService = Depends(get_user_service),
    user_description: UserDescription = Depends(get_current_user),
):
    user_service.reset_user_answered_questions(set(reset_questions), user_description)


@app.get("/categories", response_model=GetCategoriesOutput)
def get_categories(question_service: QuestionService = Depends(get_question_service)):
    """
    Get the categories.
    """
    return question_service.get_categories()


@app.get("/categories/questions", response_model=list[int])
def get_categories_questions(
    categories: list[str] = Query(..., description="List of categories to filter by"),
    question_service: QuestionService = Depends(get_question_service),
):
    return question_service.get_categories_questions(categories)


@app.get("/question/{question_id}", response_model=GetQuestionOutput)
def get_question(
    question_id: int, question_service: QuestionService = Depends(get_question_service)
):
    """
    Get a specific question with its stats.
    """
    question = question_service.get_question(question_id)

    if question is None:
        raise HTTPException(status_code=404, detail="Question not found")

    return question


@app.get("/question_next", response_model=GetQuestionOutput)
def get_next_question(
    categories: list[str] | None = Query(
        None, description="List of categories to filter by"
    ),
    question_service: QuestionService = Depends(get_question_service),
    user_service: UserService = Depends(get_user_service),
    user_description: UserDescription = Depends(get_current_user),
):
    """
    Get the next question with its stats.
    Returns a random question that hasn't been answered yet.
    """
    question, reset_questions = question_service.get_random_question(
        categories, user_description
    )
    user_service.reset_user_answered_questions(reset_questions, user_description)

    return question


@app.get("/question_stats/{question_id}", response_model=AnswerOutput)
def get_question_stats(
    question_id: int, question_service: QuestionService = Depends(get_question_service)
):
    """
    Get the stats for a question.
    """
    return question_service.get_question_stats(question_id)


@app.post("/submit_answer", response_model=AnswerOutput)
def submit_answer(
    answer: AnswerInput,
    question_service: QuestionService = Depends(get_question_service),
    user_service: UserService = Depends(get_user_service),
    user_description: UserDescription = Depends(get_current_user),
):
    """
    Submit an answer for a question and update its stats.
    Requires authentication.
    """
    answer_output = question_service.submit_answer(answer)
    user_service.answer_question(user_description, answer.question_id)

    return answer_output


@app.post("/submit_answer_multiplayer", response_model=MultiplayerResultsOutput)
def submit_answer_multiplayer(
    results: MultiplayerResultsInput,
    question_service: QuestionService = Depends(get_question_service),
    user_service: UserService = Depends(get_user_service),
    user_description: UserDescription = Depends(get_current_user),
):
    """
    Submit answers for a question and return the outlier value.
    Requires authentication.
    """
    for answer in results.answers:
        question_service.submit_answer(
            AnswerInput(question_id=results.question_id, answer=answer)
        )

    user_service.answer_question(user_description, results.question_id)

    answer_output = question_service.get_question_stats(results.question_id)

    mini = min(results.answers)
    maxi = max(results.answers)

    if abs(answer_output.average_answer - mini) > abs(
        answer_output.average_answer - maxi
    ):
        outlier_value = mini
    else:
        outlier_value = maxi

    return MultiplayerResultsOutput(
        average_answer=answer_output.average_answer,
        number_of_answers=answer_output.number_of_answers,
        outlier_value=outlier_value,
    )
