import os

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, UploadFile
from fastapi_pagination import Page
from sqlalchemy.ext.asyncio import AsyncSession

from .dependencies import get_async_session
from .schemas import PictureBase, CustomParams
from .service import picture_service


router = APIRouter()
load_dotenv()


@router.get('/all', response_model=Page[PictureBase])
async def get_all_products(
        params: CustomParams = Depends(),
        session: AsyncSession = Depends(get_async_session)
):
    """
    Запросить все изображения
    """
    return await picture_service.get_all_pictures(params, session)


@router.get('/picture/{name}', response_model=PictureBase)
async def get_picture(
        name: str,
        session: AsyncSession = Depends(get_async_session)
):
    """
    Найти изображение по имени
    """
    picture = await picture_service.get_picture_by_name(session, name)
    if picture is None:
        raise HTTPException(status_code=404, detail='Изображений с таким именем не найдено')
    return picture


@router.post('/upload_picture/', response_model=PictureBase)
async def upload_picture(
    file: UploadFile,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Загрузить изображение на сервер
    """
    filename = file.filename
    file_size = len(await file.read())
    contents = await file.read()
    picture = await picture_service.save_picture_to_database(session, filename, file_size)

    upload_folder = os.getenv('UPLOAD_FOLDER')
    file_path = os.path.join(upload_folder, filename)
    with open(file_path, 'wb') as f:
        f.write(contents)

    return picture
