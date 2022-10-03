from ariadne import QueryType, convert_kwargs_to_snake_case

from app.core.auth import get_current_user
from app.database.connection import manage_session
from app.services.todo import todo_crud_service
from app.errors import GraphQLErrorWithHTTPCode


@convert_kwargs_to_snake_case
async def resolve_todos(obj, info):
    async with manage_session() as session:
        user = await get_current_user(info, session)
        todos = await todo_crud_service.get_multi_filter(session, user_id=user.id)
    return {
        "todos": todos
    }


@convert_kwargs_to_snake_case
async def resolve_todo(obj, info, id):
    numeric_id = int(id)
    async with manage_session() as session:
        user = await get_current_user(info, session)
        todo = await todo_crud_service.get_by_id(session, numeric_id)

    if not todo:
        raise GraphQLErrorWithHTTPCode(code=404, message=f"todo id {id} not found")

    if user.id != todo.user_id:
        raise GraphQLErrorWithHTTPCode(code=403, message=f"Detail view is opened only for todo creator")

    return {
        "todo": todo
    }

query = QueryType()
query.set_field("todos", resolve_todos)
query.set_field("todo", resolve_todo)
