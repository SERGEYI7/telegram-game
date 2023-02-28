from aiohttp_apispec import querystring_schema, request_schema, response_schema
from app.quiz.schemes import (
    ListQuestionSchema,
    QuestionSchema,
    ThemeIdSchema,
    ThemeListSchema,
    ThemeSchema,
)
from app.quiz.models import Answer
from app.web.app import View
from app.web.mixins import AuthRequiredMixin
from app.web.utils import json_response
from app.web.middlewares import HTTPNotImplemented


class ThemeAddView(AuthRequiredMixin, View):
    @request_schema(ThemeSchema)
    @response_schema(ThemeSchema)
    async def post(self):
        await super().post()
        cookie = self.request.cookies
        data = await self.request.json()
        title = data.get("title")
        await self.store.quizzes.check_double_title(title)
        await self.store.quizzes.create_theme(title)
        theme = await self.store.quizzes.get_theme_by_title(title)
        return json_response(data={"id": theme.id, "title": theme.title})


class ThemeListView(AuthRequiredMixin, View):
    @response_schema(ThemeListSchema)
    async def get(self):
        await super().post()
        themes = await self.store.quizzes.list_themes()
        return json_response(data={"themes": themes})

    async def post(self):
        raise HTTPNotImplemented


class QuestionAddView(AuthRequiredMixin, View):
    @request_schema(QuestionSchema)
    @response_schema(QuestionSchema)
    async def post(self):
        await super().post()
        data = await self.request.json()
        title = data.get("title")
        theme_id = data.get("theme_id")
        answers = data.get("answers")
        await self.store.quizzes.check_valid_answers(answers)
        await self.store.quizzes.check_double_theme(theme_id=theme_id)
        question = await self.store.quizzes.create_question(
            title,
            theme_id,
            [
                Answer(title=answer.get("title"), is_correct=answer.get("is_correct"))
                for answer in answers
            ],
        )
        question_json = {
            "id": question.id,
            "title": question.title,
            "theme_id": question.theme_id,
            "answers": [
                {"title": answer.title, "is_correct": answer.is_correct}
                for answer in question.answers
            ],
        }

        return json_response(data=question_json)


class QuestionListView(AuthRequiredMixin, View):
    @querystring_schema(ThemeIdSchema)
    @response_schema(ListQuestionSchema)
    async def get(self):
        await super().post()
        questions_db = await self.store.quizzes.list_questions()
        questions = []
        for question in questions_db:
            questions.append(
                {
                    "id": question.id,
                    "title": question.title,
                    "theme_id": question.theme_id,
                    "answers": [
                        {"title": answer.title, "is_correct": answer.is_correct}
                        for answer in question.answers
                    ],
                }
            )
        return json_response(data={"questions": questions})
