# pull official base image
FROM python:3.9-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN set -eux \
  && apk add --no-cache --virtual .build-deps build-base \
  libressl-dev libffi-dev gcc musl-dev python3-dev postgresql-dev

# copy requirements file
COPY requirements.txt ./requirements.txt

RUN pip install --upgrade pip setuptools wheel \
  && pip install -r /usr/src/app/requirements.txt \
  && rm -rf /root/.cache/pip

# copy project
COPY . .
