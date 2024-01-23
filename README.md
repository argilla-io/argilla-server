# argilla-server

The repository for backend argilla server.

## Clone repository

`argilla-server` is using `argilla` as submodule to build frontend statics so when cloning use the following:

```sh
git clone --recurse-submodules git@github.com:argilla-io/argilla-server.git
```

If you already cloned the repository without using `--recurse-submodules` you can init and update the submodules with:

```sh
git submodule update --recursive --init
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

### Build frontend static files

Before running Argilla development server we need to build the frontend static files. Node version 18 is required for this action:

```sh
brew install node@18
```

After that you can build the frontend static files:

```sh
./scripts/build_frontend.sh
```

After running the previous script you should have a folder at `src/argilla_server/static` with all the frontend static files successfully generated.

### Run uvicorn development server

```sh
pdm run uvicorn argilla_server:app --reload
```
