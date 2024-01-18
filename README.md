# argilla-server

The repository for backend argilla server.

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
