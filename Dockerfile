FROM python:3.8-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV TZ Europe/Moscow

WORKDIR /usr/src/app/
COPY . /usr/src/app/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000
