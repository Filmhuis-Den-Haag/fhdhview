FROM python:3.14-slim AS builder

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true

RUN pip install --upgrade pip
RUN pip install poetry

WORKDIR /app

COPY poetry.lock pyproject.toml ./

RUN poetry install --only main --no-root


FROM python:3.14-slim AS runtime

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN adduser --disabled-password --gecos "" appuser

WORKDIR /app

COPY --from=builder /app/pyproject.toml /app/poetry.lock ./
COPY . /app
COPY --from=builder /app/.venv /app/.venv

RUN mkdir -p /data && chown appuser:appuser /data
RUN apt update && apt install -y curl

ENV PATH="/app/.venv/bin:$PATH"

USER appuser

EXPOSE 8000
CMD ["uvicorn", "fhdhview.main:app", "--host", "0.0.0.0", "--port", "8000"]
