FROM python:3.9.10-slim as build

RUN apt-get update \
	&& apt-get install libffi-dev netcat \
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
ENV POETRY_VERSION=1.2.2
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

RUN poetry install --no-root

COPY . .

FROM python:3.9.10-slim

RUN apt-get update && apt-get install -y netcat && apt-get clean

ENV PYTHONDONTWRITEBYTECODE 1 
ENV PYTHONUNBUFFERED 1 
ENV APP_HOME="/app"

WORKDIR $APP_HOME

ENV POETRY_HOME="/opt/poetry"
ENV VENV_DIR="${APP_HOME}/.venv"

# Copy the app directory(source code and venv folders)
COPY --from=build $APP_HOME $APP_HOME
# Copy peotry too just incase we need the cli
COPY --from=build $POETRY_HOME $POETRY_HOME

# Update path with poetry and venv cli apps
ENV PATH="$POETRY_HOME/bin:$VENV_DIR/bin:$PATH"

RUN chmod +x api.sh

CMD ["./api.sh"]
