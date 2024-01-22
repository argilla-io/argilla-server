# argilla-server

The repository for backend argilla server.

## Clone repository

`argilla-server` is using `argilla` as submodule to build frontend statics so when cloning use the following:

```sh
git clone --recurse-submodules git@github.com:argilla-io/argilla-server.git
```

## Run database migrations

```sh
pdm run alembic -c src/argilla_server/alembic.ini upgrade head
```

## Run tests

```sh
pdm run pytest
```

## Run cli

```sh
pdm run python -m argilla_server.cli
```

## Run development server

```sh
pdm run uvicorn argilla_server:app --reload
```
