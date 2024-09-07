FROM python:3.10.0-slim as build

RUN apt-get update \
	&& apt-get install libffi-dev \
	gcc python3-dev libpq-dev curl build-essential -y \
	&& apt-get clean

ENV APP_HOME="/app"

WORKDIR $APP_HOME

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1 
ENV PYTHONUNBUFFERED 1 
ENV PIP_NO_CACHE_DIR=off 
ENV PIP_DISABLE_PIP_VERSION_CHECK=on 
ENV PIP_DEFAULT_TIMEOUT=100

# poetry
# https://python-poetry.org/docs/configuration/#using-environment-variables
ENV POETRY_VERSION=1.8.3
# make poetry install to this location
ENV POETRY_HOME="/opt/poetry"
ENV POETRY_VIRTUALENVS_PATH=".venv" 
ENV POETRY_VIRTUALENVS_IN_PROJECT=true 
ENV POETRY_NO_INTERACTION=1
ENV VENV_DIR=$APP_HOME/.venv/

# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$APP_HOME/.venv/bin:$PATH"

# install poetry - respects $POETRY_VERSION & $POETRY_HOME
RUN curl -sSL https://install.python-poetry.org | python

COPY poetry.lock pyproject.toml ./

RUN poetry install

COPY . .

# ================================ Main Build ================================

FROM python:3.10.0-slim

RUN apt-get update && apt-get install -y netcat && apt-get clean

ENV PYTHONDONTWRITEBYTECODE 1 
ENV PYTHONUNBUFFERED 1 
ENV APP_HOME="/app"

WORKDIR $APP_HOME

ENV POETRY_HOME="/opt/poetry"
ENV VENV_DIR="${APP_HOME}/.venv"

COPY --from=build $APP_HOME $APP_HOME
COPY --from=build $POETRY_HOME $POETRY_HOME

ENV PATH="$POETRY_HOME/bin:$VENV_DIR/bin:$PATH"

RUN chmod +x ./k8s/scripts/api.sh
RUN chmod +x ./k8s/scripts/migrate-db.sh

CMD ["./k8s/scripts/api.sh"]
