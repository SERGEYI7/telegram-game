import typing

from sqlalchemy import select

from app.admin.models import Admin, AdminModel
from app.base.base_accessor import BaseAccessor

if typing.TYPE_CHECKING:
    from app.web.app import Application


class AdminAccessor(BaseAccessor):
    async def get_by_email(self, email: str) -> Admin | None:
        async with self.app.database.session() as session:
            async with session.begin():
                result = await session.execute(
                    select(AdminModel).where(AdminModel.email == email)
                )
                admin_model = result.scalars().all()
        if admin_model:
            admin = admin_model[0]
            return Admin(id=admin.id, email=admin.email, password=admin.password)
        else:
            return admin_model

    async def create_admin(self, email: str, password: str) -> Admin:
        async with self.app.database.session() as session:
            async with session.begin():

                admin_model = AdminModel(email=email, password=password)
                session.add(admin_model)
                # await session.commit()
            admin = await self.get_by_email(email)
        return Admin(id=admin.id, email=admin.email, password=admin.password)
