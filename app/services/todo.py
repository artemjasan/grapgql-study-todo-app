from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.base import CRUDBase
from app.database import schema


class CRUDTodo(CRUDBase):
    async def get_by_id(self, session: AsyncSession, id: int) -> schema.Todo | None:
        return await super().get(session, id=id)

    async def get_multi_filter(self, session: AsyncSession, user_id: int) -> list[schema.Todo | None]:
        response =\
            await session.execute(select(self.model).where(self.model.user_id == user_id).order_by(self.model.id.desc()))
        return response.scalars().all()

    async def create(self, session: AsyncSession, **kwargs) -> schema.Todo:
        db_obj = schema.Todo(
            description=kwargs["description"],
            completed=kwargs["completed"],
            date=kwargs["date"],
            user_id=kwargs["user_id"]
        )
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj


todo_crud_service = CRUDTodo(schema.Todo)
