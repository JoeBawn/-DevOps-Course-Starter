FROM python:3 as base

WORKDIR /app
COPY ./poetry.toml /app
COPY ./pyproject.toml /app
RUN pip install poetry && poetry install

FROM base as production
COPY ./todo_app /app/todo_app
EXPOSE 5000
ENTRYPOINT poetry run gunicorn --error-logfile /app/error.log -b 0.0.0.0:5000 "todo_app.app:create_app()"

FROM base as development
EXPOSE 5000
ENTRYPOINT  poetry run flask run --host 0.0.0.0

FROM base as test 
RUN pip install poetry && poetry install
COPY ./todo_app /app/todo_app
ENTRYPOINT [ "poetry", "run", "pytest" ]