# Notes App

A note taking application that exposes a RESTful webservice interface which allows users be able to create simple notes.

## Running the API

Build the images and run the containers:

```sh
$ docker-compose up -d --build
```

Test out the following routes:

1. [http://localhost:8022/docs](http://localhost:8003/docs)
1. [http://localhost:8022/notes](http://localhost:8003/notes)

## Automated Tests

Run automated integrated tests with the following commands

```sh
$ docker-compose run api python -m pytest
```

## Built With

The project has been built with the following technologies so far:

- [FastAPI](https://fastapi.tiangolo.com/) - FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints.
- [PostgreSQL](https://www.postgresql.org/) - A production-ready relational database system emphasizing extensibility and technical standards compliance.
- [Pydantic](https://pydantic-docs.helpmanual.io/) - A data validation and settings management tool using python type annotations.
