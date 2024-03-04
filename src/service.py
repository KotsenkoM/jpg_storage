from fastapi import HTTPException
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from typing import Sequence

from src.models.models import Picture
from .schemas import PictureBase, CustomParams


class PictureService:
    def __init__(self, model):
        self.model = model

    async def get_picture_by_name(self, session: AsyncSession, name: str) -> Picture | None:
        stmt = (
            select(self.model)
            .where(self.model.name == name)
        )
        product_db = await session.execute(stmt)
        return product_db.scalars().first()

    async def get_picture_by_id(self, session: AsyncSession, id: int) -> Picture | None:
        stmt = (
            select(self.model)
            .where(self.model.id == id)
        )
        product_db = await session.execute(stmt)
        return product_db.scalars().first()

    async def get_all_pictures(self, params: CustomParams, session: AsyncSession) -> Sequence[PictureBase]:
        stmt = (
            select(self.model)
            .order_by(
                desc(self.model.name),
            )
        )
        pictures_db = await paginate(conn=session, query=stmt, params=params)
        return pictures_db

    async def save_picture_to_database(self, session: AsyncSession, name: str, size: int) -> Picture:
        picture = await self.get_picture_by_name(session, name)
        if picture:
            raise HTTPException(status_code=400, detail='Файл с таким именем уже существует')
        else:
            picture = Picture(name=name, size=size)
        session.add(picture)
        await session.commit()
        return picture

    async def delete_picture_by_id(self, session: AsyncSession, id: int) -> Picture:
        picture = await self.get_picture_by_id(session, id)
        if picture is None:
            raise HTTPException(status_code=404, detail='Изображения с таким id не найдено')
        else:
            await session.delete(picture)
            await session.commit()
        return picture


picture_service = PictureService(Picture)
