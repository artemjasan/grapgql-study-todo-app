# pull official base image
FROM python:3.10-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV DEBUG 1

# Install build dependencies missing on Alpine.
RUN apk add --no-cache build-base libffi-dev bash

# set working directory
WORKDIR /graphql-study-todo-app

# Copy dependencies from poetry
COPY pyproject.toml poetry.lock ./

# install python dependencie
RUN pip install --upgrade pip setuptools poetry
RUN poetry config virtualenvs.create false
RUN poetry install

# add app
COPY . .