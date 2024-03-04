FROM python:3.10-alpine
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
RUN mkdir /jpg_storage
COPY requirements.txt /jpg_storage
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /jpg_storage/requirements.txt
COPY . .
RUN mkdir /jpg_storage/uploads
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]