from aiohttp.web import (
    HTTPForbidden,
    HTTPUnauthorized,
    HTTPNotImplemented,
    HTTPBadRequest,
)
from aiohttp_apispec import request_schema, response_schema
from aiohttp_session import new_session

from app.admin.schemes import AdminSchema
from app.web.app import View
from app.web.utils import json_response, error_json_response
from app.web.mixins import AuthRequiredMixin
from hashlib import sha256
from base64 import b64encode


class AdminLoginView(View):
    @request_schema(AdminSchema)
    @response_schema(AdminSchema, 200)
    async def post(self):
        email = self.data.get("email")
        id_ = self.data.get("id")
        password = sha256(self.data.get("password").encode()).hexdigest()
        admin = await self.store.admins.get_by_email(email)
        if not email:
            return error_json_response(
                http_status=400,
                status="bad_request",
                data={"data": "Missing data for required field."},
            )
        if not admin:
            # await self.store.admins.create_admin(email, password)
            # admin = await self.store.admins.get_by_email(email)
            raise HTTPForbidden
        response = json_response(data={"email": admin.email, "id": admin.id})
        email_password = f"{email}:{password}"
        response.set_cookie("session_id", b64encode(email_password.encode()).decode())
        return response

    @request_schema(AdminSchema)
    @response_schema(AdminSchema)
    async def get(self):
        raise HTTPNotImplemented


class AdminCurrentView(View):
    @response_schema(AdminSchema, 200)
    async def get(self):
        raise NotImplementedError
