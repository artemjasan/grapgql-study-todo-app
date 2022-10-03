# Todo app with GraphQL and FastAPI
A Small todo application to study GraphQL and integration with python projects.

## Start here

For that project I've used the following technologies:
- [Python 3.10](https://www.python.org/downloads/release/python-3104/)
- [Poetry](https://python-poetry.org/) modern and powerful package manager
- [Ariadne](https://ariadnegraphql.org/) schema-first GraphQL framework
- [FastAPI](https://fastapi.tiangolo.com/) backend framework
- [Postgres](https://www.postgresql.org/) main project database
- [Docker](https://www.docker.com/) & [Docker Compose](https://www.docker.com/) Containerized development tools


It's start of your journey on this project.
For convenience, I use local containerization using `Docker` and `Docker Composes.`
It's easy and fast and provides a good level of isolation, but there are a few steps 
to follow before using Docker:

**Install poetry package manager to your machine**
```shell
$ pip install poetry
```
**Activate poetry**
```shell
$ poetry shell
```
**Install dependencies to venv**
```shell
$ poetry install
```
## Launch application by `Docker`/`Docker Compose`
Build Docker image:
```shell
$ docker-compose build
$ docker-compose up
```
Open another terminal session and run migrations:

```shell
$ docker-compose exec web_app alembic upgrade head
```



## How to use the application
> Firstly you should create user and login
> has basic authentication system, which based on JWT.

> Returned Bearer Token put in to HTTP HEADERS in format:
```
{
  "Authorization": "Bearer <JWT Token>"
}
```
#### Play end enjoy ;)
**General endpoint**
`http://0.0.0.0:8000/`

