FROM python:3.12-slim

RUN apt-get update && apt-get install

RUN apt-get install curl -y

WORKDIR /app

COPY app/ /app/

RUN pip install -r requirements.txt

WORKDIR /
