from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.secure import verify_password

from app.services.base import CRUDBase
from app.database import schema


class CRUDUser(CRUDBase):
    async def get_by_id(self, session: AsyncSession, id: int) -> schema.User | None:
        return await super().get(session, id=id)

    async def get_by_email(self, session: AsyncSession, email: str) -> schema.User | None:
        response = await session.execute(select(self.model).where(self.model.email == email))
        return response.scalar()

    async def create(self, session: AsyncSession, **kwargs) -> schema.User:
        db_obj = schema.User(
            email=kwargs["email"],
            hashed_password=kwargs["hashed_password"]
        )
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def authenticate(self, session: AsyncSession, email: str, password: str) -> schema.User | None:
        actual_user = await self.get_by_email(session=session, email=email)
        if not actual_user:
            return None
        if not verify_password(plain_password=password, hashed_password=actual_user.hashed_password):
            return None

        return actual_user


user_crud_service = CRUDUser(schema.User)
