FROM python:3.12

WORKDIR /opt/app/

COPY poetry.lock /opt/app/poetry.lock
COPY pyproject.toml /opt/app/pyproject.toml

RUN pip install poetry

RUN poetry config virtualenvs.create false && poetry install --no-root

COPY ./src /opt/app/src

WORKDIR /opt/app/src

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "80"]
