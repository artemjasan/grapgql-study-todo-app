from typing import Any, TypeVar, Type

from fastapi.encoders import jsonable_encoder

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database.schema import Base

ModelType = TypeVar("ModelType", bound=Base)


class CRUDBase:
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with defaults methods to Create, Read, Update, Delete actions
        """
        self.model = model

    async def get(self, session: AsyncSession, id: int) -> ModelType | None:
        response = await session.execute(select(self.model).where(self.model.id == id))
        return response.scalar()

    async def get_multi(self, session: AsyncSession) -> list[ModelType | None]:
        response = await session.execute(select(self.model).order_by(self.model.id.desc()))
        return response.scalars().all()

    async def create(self, session: AsyncSession, **kwargs) -> ModelType:
        obj_in_data = jsonable_encoder(**kwargs)
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(
            self, session: AsyncSession, obj_current: ModelType, **kwargs) -> ModelType:
        obj_in = kwargs
        obj_data = jsonable_encoder(obj_current)
        for field in obj_data:
            if field in obj_in:
                setattr(obj_current, field, obj_in[field])
        session.add(obj_current)
        await session.commit()
        await session.refresh(obj_current)
        return obj_current

    async def delete(self, session: AsyncSession, id: int) -> ModelType:
        response = await self.get(session=session, id=id)
        await session.delete(response)
        await session.commit()
        return response
