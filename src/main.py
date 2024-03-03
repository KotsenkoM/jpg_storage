from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .router import router

app = FastAPI()

app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=(
        'HEAD',
        'OPTIONS',
        'GET',
        'POST',
        'DELETE',
        'PATCH',
    ),
    allow_headers=('*'),
)
