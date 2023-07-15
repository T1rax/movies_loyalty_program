FROM python:3.11-buster

WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip3 install poetry==1.4.2 --no-cache-dir

COPY poetry.lock pyproject.toml /code/

RUN poetry config experimental.new-installer false && poetry config virtualenvs.create false && poetry install --no-root

COPY . /code

RUN chmod +x /code/run.sh

ENTRYPOINT ["/code/run.sh"]