FROM python:3.10.2

ENV PYTHONBUFFERED 1

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r "requirements.txt"

COPY . .