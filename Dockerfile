FROM python:3.9.5-slim as builder

RUN apt-get update \
  && apt-get install libffi-dev gcc python3-dev libpq-dev -y \
  && apt-get clean

WORKDIR /app

COPY requirements.txt /app/requirements.txt

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

ENV PATH=/opt/venv/bin:/usr/pgsql-9.1/bin/:/root/.local/bin:$PATH

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

RUN chmod +x api.sh

CMD ["bash","api.sh"]
