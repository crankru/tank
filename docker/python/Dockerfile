FROM python:3.8.8-buster

RUN apt-get update & pip install pip-tools
ADD requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

WORKDIR /code

ENV PYTHONUNBUFFERED 1