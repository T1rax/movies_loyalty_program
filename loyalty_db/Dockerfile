FROM python:3.11-slim

WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip3 install psycopg2-binary yoyo-migrations==8.2.0

COPY ./migrations ./migrations/

COPY . /code