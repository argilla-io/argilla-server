# argilla-server

The repository for backend argilla server.

## Clone repository

`argilla-server` is using `argilla` repository as submodule to build frontend statics so when cloning use the following command:

```sh
git clone --recurse-submodules git@github.com:argilla-io/argilla-server.git
```

If you already cloned the repository without using `--recurse-submodules` you can init and update the submodules with:

```sh
git submodule update --remote --recursive --init
```

> [!IMPORTANT]
> By default `argilla` submodule is using `develop` branch so the previous command will get the latest commit from that branch.

### Specify a tag for argilla submodule

When doing a release we should change `argilla` submodule to use an specific tag. In the following example we are setting tag `v1.22.0`:

```sh
cd argilla
git fetch --tags
git checkout v1.22.0
```

> [!NOTE]
> You should see some changes on the `argilla-server` root folder where the subproject commit is now changed to the one from the tag version. Feel free to commit these changes.

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
