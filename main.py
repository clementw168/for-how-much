from fastapi import Depends, FastAPI, HTTPException, Query

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
)
from for_how_much.services import QuestionService

# Create database tables if they don't exist
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="For How Much API")


def get_question_service(db=Depends(get_db)):
    return QuestionService(db=db)


@app.get("/categories", response_model=GetCategoriesOutput)
def get_categories(question_service: QuestionService = Depends(get_question_service)):
    """
    Get the categories.
    """
    return question_service.get_categories()


@app.get("/question/{question_id}", response_model=GetQuestionOutput)
def get_question(
    question_id: int, question_service: QuestionService = Depends(get_question_service)
):
    """
    Get the next question with its stats.
    Returns a random question that hasn't been answered yet.
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
):
    """
    Get the next question with its stats.
    Returns a random question that hasn't been answered yet.
    """
    question = question_service.get_random_question(categories)
    if question is None:
        raise HTTPException(status_code=404, detail="Question not found")

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
):
    """
    Submit an answer for a question and update its stats.
    """
    return question_service.submit_answer(answer)


@app.post("/multiplayer_results", response_model=MultiplayerResultsOutput)
def post_multiplayer_results(
    results: MultiplayerResultsInput,
    question_service: QuestionService = Depends(get_question_service),
):
    """
    Submit answers for a question and return the outlier value.
    """
    for answer in results.answers:
        answer_output = question_service.submit_answer(
            AnswerInput(question_id=results.question_id, answer=answer)
        )

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
