from fastapi import FastAPI
from ariadne import load_schema_from_path, make_executable_schema, snake_case_fallback_resolvers, format_error
from ariadne.asgi import GraphQL
from graphql.error.graphql_error import GraphQLError

from app.api.queries import query
from app.api.mutations import mutation


def error_format(error: GraphQLError, debug: bool = False) -> dict:
    if debug:
        return format_error(error, debug)

    formatted = error.formatted
    formatted["message"] = error.args[0]
    return formatted


def make_app() -> FastAPI:
    app = FastAPI(
        title="Study GraphQL",
        version="0.1.0",
        description="Simple To-do app with FastAPI and Ariadne"
    )

    type_defs = load_schema_from_path(path="app/graphql/schema.graphql")
    resolvers = [query, mutation]
    schema = make_executable_schema(type_defs, resolvers, snake_case_fallback_resolvers)

    graph_ql = GraphQL(schema=schema, error_formatter=error_format, debug=False)

    app.mount("/", graph_ql)

    return app
