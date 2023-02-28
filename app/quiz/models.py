from dataclasses import dataclass
from app.store.database.sqlalchemy_base import db
from sqlalchemy import Column, INTEGER, ForeignKey, CHAR, Boolean, TEXT, ARRAY
from sqlalchemy.orm import relationship, backref


@dataclass
class Theme:
    id: int | None
    title: str


@dataclass
class Question:
    id: int | None
    title: str
    theme_id: int
    answers: list["Answer"]


@dataclass
class Answer:
    title: str
    is_correct: bool


class ThemeModel(db):
    __tablename__ = "themes"
    id = Column(INTEGER, primary_key=True)
    title = Column(TEXT, unique=True)
    question = relationship(
        "QuestionModel", cascade="all, delete", passive_deletes=True
    )
    # answer = relationship("AnswerModel", cascade="all, delete-orphan")


class QuestionModel(db):
    __tablename__ = "questions"
    id = Column(INTEGER, primary_key=True)
    title = Column(TEXT, unique=True)
    theme_id = Column(
        INTEGER, ForeignKey("themes.id", ondelete="CASCADE"), nullable=False
    )
    answers = relationship(
        "AnswerModel", back_populates="question", lazy="subquery", cascade="all, delete"
    )


class AnswerModel(db):
    __tablename__ = "answers"
    id = Column(INTEGER, primary_key=True)
    title = Column(TEXT, unique=True)
    is_correct = Column(Boolean)
    question_id = Column(INTEGER, ForeignKey("questions.id", ondelete="CASCADE"))
    question = relationship("QuestionModel", back_populates="answers")
