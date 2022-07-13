FROM python:3.8.5-slim-buster
ENV PYTHONBUFFERED 1
WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

