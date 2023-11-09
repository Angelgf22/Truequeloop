# syntax=docker/dockerfile:1
FROM python:3.11

RUN apt-get update
RUN apt-get install -y python3-psycopg2
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/