from fastapi import Query
from fastapi_pagination import Params
from pydantic import BaseModel


class CustomParams(Params):
    """Пользовательские параметры для пагинации всех изображений"""

    size: int = Query(10, ge=1, le=50, description='Размер страницы')


class PictureBase(BaseModel):
    id: int
    name: str
    size: int


class GetPicture(BaseModel):
    name: str
    size: int
