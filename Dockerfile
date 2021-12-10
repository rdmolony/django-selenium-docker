FROM python:3.7.12-slim-buster
ENV PYTHONUNBUFFERED 1

WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code

VOLUME /code
