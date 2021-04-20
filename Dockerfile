FROM python:3.10.0a7-buster as base
WORKDIR /todo_app
COPY poetry.toml pyproject.toml /todo_app
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./your-daemon-or-script.py" ]