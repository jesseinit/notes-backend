# Notes App

A note taking application that exposes a RESTful webservice interface which allows users be able to create simple notes.

## Running the API

Build the images and run the containers:

```sh
make bootstrap
```

Read the API Documentation on [here](http://localhost:8023/docs)

## Automated Tests

Ensure api container is running the run automated integrated tests with

```sh
$ docker exec -it notes-api pytest
```

## Built With

The project has been built with the following technologies so far:

- [FastAPI](https://fastapi.tiangolo.com/) - FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints.
- [PostgreSQL](https://www.postgresql.org/) - A production-ready relational database system emphasizing extensibility and technical standards compliance.
- [Pydantic](https://pydantic-docs.helpmanual.io/) - A data validation and settings management tool using python type annotations.
