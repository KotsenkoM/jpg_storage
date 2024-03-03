from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator

from src.database import async_session
from src.service import picture_service


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


async def validate_picture_exists(
    id: int,
    session: AsyncSession = Depends(get_async_session)
) -> int:

    if not await picture_service.get_product(id, session):
        raise HTTPException(status_code=404)
    return id
