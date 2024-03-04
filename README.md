# jpg_storage
## Тестовое задание
API for storing *.jpg files on the server

## Задание

**Цель задания:** создать сервис на FastAPI, позволяющий хранить на сервере файлы
формата *.jpg. Файлы можно:
- Загрузить на сервер (один или несколько).
- Скачать с сервера (один или несколько, если несколько, то сервер должен упаковывать их в
архив).
- Искать по названию. В ответ приходит информация о подходящих файлах (имя и размер).
- Удалить файлы по id.
Необходимо реализовать 4 конечные точки для работы с номенклатурой.

**Требования:**
1. Использовать FastAPI, SQLAlchemy, Alembic, PostgreSQL.
2. Завернуть приложение в Docker (например, можно использовать docker-
compose), чтобы его можно было быстро развернуть у себя.

## Запуск проекта

1. Клонировать репозиторий
```shell
HTTPS
git clone https://github.com/KotsenkoM/jpg_storage.git

SSH
git clone git@github.com:KotsenkoM/jpg_storage.git
```
2. Перейти в директорию с проектом:
```shell
cd jpg_storage/
```
3. В корневой директории проекта создать файл .env и заполнить его:
```shell
DB_ENGINE=postgresql+asyncpg
DB_NAME=postgres
DB_HOST=database
DB_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
UPLOAD_DOCKER_FOLDER=/jpg_storage/uploads
UPLOAD_HOST_FOLDER=<папка в которую будут сохранятся файлы на Вашем хосте, где развернуто приложение>
```

### Unix systems
3. Выполнить команду по созданию и запуску контейнеров:
```shell
make up
```
4. Выполнить миграции:
```shell
make migrate
```
Документация к API доступна по ссылке: http://localhost:8000/docs/

Для получения полного списка доступных комманд выполните:
```shell
make help
```

### Windows
3. Запустить создание и запуск контейнеров:
```shell
docker-compose -f docker-compose.yaml up -d --build
```
4. Выполнить миграции:
```shell
docker-compose exec backend alembic upgrade head
```
Документация к API доступна по ссылке: http://localhost:8000/docs/



#### VENV
1. Установить виртуальное окружение:
```shell
python3 -m venv venv
```

2. Активировать виртуальное окружение:
```
Unix like:
source venv/bin/activate

Windows:
venv\Scripts\activate.bat
```

3. Обновить `pip` и установить зависимости:
```shell
pip3 install --upgrade pip

pip3 install -r requirements.txt
```
