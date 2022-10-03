from graphql.error.graphql_error import GraphQLError


class GraphQLErrorWithHTTPCode(GraphQLError):
    def __init__(self, message: str, code: int) -> None:
        super().__init__(message, extensions={"code": code})


