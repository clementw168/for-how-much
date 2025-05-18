from pydantic import BaseModel


class GetCategoriesOutput(BaseModel):
    categories: list[str]


class GetQuestionOutput(BaseModel):
    id: int
    text: str
    image_url: str | None = None
    type: str
    min_value: int
    max_value: int
    price_unit: str
    category: str
    average_answer: float
    number_of_answers: int


class AnswerInput(BaseModel):
    question_id: int
    answer: int


class MultiplayerResultsInput(BaseModel):
    question_id: int
    answers: list[int]


class AnswerOutput(BaseModel):
    average_answer: float
    number_of_answers: int


class MultiplayerResultsOutput(AnswerOutput):
    outlier_value: int
