FROM python:3.12.1-slim as base

ENV POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    POETRY_VERSION=2.1.0


FROM base as builder

RUN pip install --upgrade pip poetry==$POETRY_VERSION

COPY poetry.toml pyproject.toml poetry.lock README.md ./
COPY data_platform ./data_platform

RUN poetry install --no-root && \
    poetry build

FROM base as final

COPY --from=builder ./.venv ./.venv

COPY main.py uvicorn_disable_logging.json ./
COPY data_platform ./data_platform

EXPOSE 8000

# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
CMD [".venv/bin/python", "-m", "main"]