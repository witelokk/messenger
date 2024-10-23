FROM python:3.12-slim

RUN pip install poetry

ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-dev --no-interaction --no-ansi

COPY . .

EXPOSE 8000

CMD ["sh", "-c", "(cd messenger && alembic upgrade head) && uvicorn messenger.main:app --host 0.0.0.0 --port 8000 --root-path /api/"]
