from aiohttp.abc import StreamResponse
from aiohttp.web_exceptions import HTTPUnauthorized
from hashlib import sha256
from app.web.app import View
import base64
from base64 import b64encode, b64decode


class AuthRequiredMixin:
    async def post(self: View):
        # req = self.request
        cookie = self.request.cookies.get("session_id")
        if not cookie:
            raise HTTPUnauthorized
        # data = await self.request.json()
        email, password = b64decode(cookie).decode().split(":")
        print(email, password)
        admin_in_db = await self.store.admins.get_by_email(email)
        if admin_in_db.password != password:
            raise HTTPUnauthorized
        # email = data.get("email")
        # raw_password = data.get("password")
        # password = sha256(raw_password.encode()).hexdigest()
        # headers = self.request.raw_headers
        # cookie = self.request.cookies
        # existing_password = await self.store.admins.get_by_email(email).password
        # if password != existing_password:
        #     raise HTTPUnauthorized
        # b64encode(f"{email}:{raw_password}")
