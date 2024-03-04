import os
import zipfile

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, UploadFile
from fastapi_pagination import Page
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import FileResponse
from typing import List

from .dependencies import get_async_session
from .schemas import CustomParams, GetPicture, PictureBase
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


@router.get('/picture/{name}', response_model=GetPicture)
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


@router.post('/upload_picture/', response_model=List[PictureBase])
async def upload_picture(
    files: List[UploadFile],
    session: AsyncSession = Depends(get_async_session),
):
    """
    Загрузить изображение на сервер
    """
    pictures = []
    for file in files:
        filename, file_extension = os.path.splitext(file.filename)
        if file_extension.lower() != '.jpg':
            raise HTTPException(status_code=400, detail='Файл должен быть в формате JPG')

        file_size = len(await file.read())
        picture = await picture_service.save_picture_to_database(session, file.filename, file_size)

        upload_folder = os.getenv('UPLOAD_FOLDER')
        file_path = os.path.join(upload_folder, file.filename)
        with open(file_path, 'wb') as f:
            file.file.seek(0)
            contents = await file.read()
            f.write(contents)
        pictures.append(picture)
    return pictures


@router.delete('/delete_picture/{id}')
async def delete_picture(
    id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Удалить изображение из сервера и запись о нем из БД по его id
    """

    picture = await picture_service.delete_picture_by_id(session, id)
    if picture is None:
        raise HTTPException(status_code=404, detail='Изображение не найдено')

    upload_folder = os.getenv('UPLOAD_FOLDER')
    file_path = os.path.join(upload_folder, picture.name)
    if os.path.exists(file_path):
        os.remove(file_path)
    else:
        raise HTTPException(status_code=404, detail='Изображение не найдено')

    return {"message": "Изображение успешно удалено"}


@router.get('/download_picture/{id}')
async def download_picture(
    id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Скачать изображение по его id
    """

    picture = await picture_service.get_picture_by_id(session, id)
    if picture is None:
        raise HTTPException(status_code=404, detail='Изображение не найдено')

    upload_folder = os.getenv('UPLOAD_FOLDER')
    file_path = os.path.join(upload_folder, picture.name)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type='application/octet-stream', filename=picture.name)
    else:
        raise HTTPException(status_code=404, detail='Файл не найден')


@router.post('/download_pictures/')
async def download_pictures(
    ids: List[int],
    session: AsyncSession = Depends(get_async_session),
):
    """
    Скачать изображения с сервера по их id
    """
    pictures = []
    for id in ids:
        picture = await picture_service.get_picture_by_id(session, id)
        if picture:
            pictures.append(picture)
        else:
            raise HTTPException(status_code=404, detail=f'Изображение с id={id} не найдено')

    if len(pictures) == 1:
        picture = pictures[0]
        upload_folder = os.getenv('UPLOAD_FOLDER')
        file_path = os.path.join(upload_folder, picture.name)
        return FileResponse(file_path, filename=picture.name)
    elif len(pictures) > 1:
        zip_filename = "pictures.zip"
        with zipfile.ZipFile(zip_filename, "w") as zip_file:
            for picture in pictures:
                upload_folder = os.getenv('UPLOAD_FOLDER')
                file_path = os.path.join(upload_folder, picture.name)
                zip_file.write(file_path, picture.name)

        return FileResponse(zip_filename, filename=zip_filename)
    else:
        raise HTTPException(status_code=400, detail='Не указаны id изображений для скачивания')
