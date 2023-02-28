from app.base.base_accessor import BaseAccessor
from app.quiz.models import (
    Answer,
    Question,
    Theme,
    ThemeModel,
    AnswerModel,
    QuestionModel,
)
from app.web.middlewares import HTTPConflict, HTTPNotFound, HTTPBadRequest
from sqlalchemy import select


class QuizAccessor(BaseAccessor):
    async def create_theme(self, title: str) -> Theme:
        async with self.app.database.session() as session:
            async with session.begin():
                session.add(ThemeModel(title=title))
        theme = await self.get_theme_by_title(title)
        return theme

    async def check_double_title(self, title: str) -> None:
        async with self.app.database.session() as session:
            async with session.begin():
                stml = select(ThemeModel).where(ThemeModel.title == title)
                query = (await session.scalars(stml)).all()
                if query:
                    raise HTTPConflict

    async def get_theme_by_title(self, title: str) -> Theme | None:
        async with self.app.database.session() as session:
            async with session.begin():
                stml = select(ThemeModel).where(ThemeModel.title == title)
                query = await session.scalars(stml)
                theme = query.first()
        if theme:
            return Theme(id=theme.id, title=theme.title)
        return theme

    async def get_theme_by_id(self, id_: int) -> Theme | None:
        async with self.app.database.session() as session:
            async with session.begin():
                stml = select(ThemeModel).where(ThemeModel.id == id_)
                query = await session.scalars(stml)
                theme = query.first()
        if theme:
            return Theme(id=theme.id, title=theme.title)
        return theme

    async def list_themes(self) -> list[Theme]:
        async with self.app.database.session() as session:
            async with session.begin():
                themes = (await session.scalars(select(ThemeModel))).all()
        ready_themes = []
        for theme in themes:
            ready_themes.append({"id": theme.id, "title": theme.title})
        return ready_themes

    async def create_answers(
        self, question_id: int, answers: list[Answer]
    ) -> list[Answer]:
        async with self.app.database.session() as session:
            async with session.begin():
                session.add(AnswerModel)

    async def check_double_theme(self, theme_id):
        async with self.app.database.session() as session:
            stml = select(ThemeModel).where(ThemeModel.id == theme_id)
            theme = (await session.scalars(stml)).all()
            if not theme:
                raise HTTPNotFound

    async def check_valid_answers(self, answers: list[dict]):
        list_correct = [correct.get("is_correct") for correct in answers]
        if (
            (len(list_correct) == 1)
            or (True not in list_correct)
            or (False not in list_correct)
        ):
            raise HTTPBadRequest

    async def create_question(
        self, title: str, theme_id: int, answers: list[Answer]
    ) -> Question:
        answers_db = []
        for answer in answers:
            try:
                answers_db.append(
                    AnswerModel(title=answer.title, is_correct=answer.is_correct)
                )
            except Exception as e:
                print(e)
        async with self.app.database.session() as session:
            async with session.begin():
                # if not theme_id:#(await session.scalars(select(ThemeModel).where(ThemeModel.id == theme_id))).all():
                #     raise HTTPNotFound
                question = QuestionModel(
                    title=title, theme_id=theme_id, answers=answers_db
                )
                session.add_all([question])
        if not await self.get_theme_by_id(theme_id):
            raise HTTPNotFound
        question = await self.get_question_by_title(title)
        return question

    async def get_question_by_title(self, title: str) -> Question | None:
        async with self.app.database.session() as session:
            async with session.begin():
                stml = select(QuestionModel).where(QuestionModel.title == title)
                question_models = (await session.scalars(stml)).all()
        question = Question(
            id=question_models[0].id,
            title=question_models[0].title,
            theme_id=question_models[0].theme_id,
            answers=[
                Answer(answer.title, answer.is_correct)
                for answer in question_models[0].answers
            ],
        )
        return question

    async def list_questions(self, theme_id: int | None = None) -> list[Question]:
        async with self.app.database.session() as session:
            async with session.begin():
                if theme_id:
                    stml = select(QuestionModel).where(
                        QuestionModel.theme_id == theme_id
                    )
                else:
                    stml = select(QuestionModel)
                questions_db = (await session.scalars(stml)).all()
        questions = []
        for question_db in questions_db:
            id_ = question_db.id
            title = question_db.title
            theme_id = question_db.theme_id
            answers = [
                Answer(title=answer.title, is_correct=answer.is_correct)
                for answer in question_db.answers
            ]
            questions.append(
                Question(id=id_, title=title, theme_id=theme_id, answers=answers)
            )

        return questions
