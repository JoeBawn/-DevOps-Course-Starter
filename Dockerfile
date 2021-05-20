FROM python:3 as base

WORKDIR /temp
COPY ./poetry.toml /temp
COPY ./pyproject.toml /temp
RUN pip install poetry && poetry install

FROM base as production
RUN apt-get update
COPY ./todo_app /temp/todo_app
EXPOSE 5000
ENTRYPOINT $(poetry env info --path)/bin/gunicorn --error-logfile /temp/error.log -b 0.0.0.0:5000 "todo_app.app:create_app()"

FROM base as development
EXPOSE 5000
ENTRYPOINT  poetry run flask run --host 0.0.0.0


