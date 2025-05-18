from sqlalchemy import JSON, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from for_how_much.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    questions_seen = Column(Integer, default=0)
    answered_questions = Column(JSON, default=list)


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(500))
    image_url = Column(String(255), nullable=True)
    type = Column(String("slider"))  # 'slider'
    min_value = Column(Integer)
    max_value = Column(Integer)
    price_unit = Column(String("€"))
    category = Column(String("food"))

    stats = relationship("Stats", back_populates="question")


class Stats(Base):
    __tablename__ = "stats"

    question_id = Column(Integer, ForeignKey("questions.id"), primary_key=True)
    average_answer = Column(Float, default=0.0)
    number_of_answers = Column(Integer, default=0)

    question = relationship("Question", back_populates="stats")
