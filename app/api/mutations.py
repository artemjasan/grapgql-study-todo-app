import datetime

from ariadne import MutationType, convert_kwargs_to_snake_case
from sqlalchemy.exc import IntegrityError

from app.core.auth import get_current_user
from app.core.secure import get_password_hash, create_access_token
from app.core.config import settings
from app.database.connection import manage_session
from app.services.todo import todo_crud_service
from app.services.user import user_crud_service
from app.errors import GraphQLErrorWithHTTPCode


@convert_kwargs_to_snake_case
async def resolve_create_todo_item(obj, info, description, date):
    async with manage_session() as session:
        user = await get_current_user(info, session)

        response = await todo_crud_service.create(
            session,
            description=description,
            completed=False,
            date=datetime.date.fromisoformat(date),
            user_id=user.id
        )

    return {
        "todo": response
    }


@convert_kwargs_to_snake_case
async def resolve_delete_todo_item(obj, info, id):
    numeric_id = int(id)
    async with manage_session() as session:
        user = await get_current_user(info, session)
        todo_item = await todo_crud_service.get_by_id(session=session, id=numeric_id)

        if not todo_item:
            raise GraphQLErrorWithHTTPCode(code=404, message=f"todo id {numeric_id} not found")

        if user.id != todo_item.user_id:
            raise GraphQLErrorWithHTTPCode(code=403, message=f"You can delete only your own todo items")

        await todo_crud_service.delete(session, id=numeric_id)

    return {
        "errors": None
    }


@convert_kwargs_to_snake_case
async def resolve_mark_done_todo_item(obj, info, id):
    numeric_id = int(id)
    async with manage_session() as session:
        user = await get_current_user(info, session)
        current_object = await todo_crud_service.get_by_id(session, id=numeric_id)

        if not current_object:
            raise GraphQLErrorWithHTTPCode(code=404, message=f"todo id {id} not found")

        if user.id != current_object.user_id:
            raise GraphQLErrorWithHTTPCode(code=403, message=f"You can delete only your own todo items")

        response = await todo_crud_service.update(
            session,
            obj_current=current_object,
            completed=True
        )

    return {
        "todo": response
    }


@convert_kwargs_to_snake_case
async def resolve_update_todo_item(obj, info, id, description=None, date=None):
    numeric_id = int(id)
    new_data = {}
    async with manage_session() as session:
        user = await get_current_user(info, session)
        current_object = await todo_crud_service.get_by_id(session, id=numeric_id)

        if not current_object:
            raise GraphQLErrorWithHTTPCode(code=404, message=f"todo id {id} not found")

        if user.id != current_object.user_id:
            raise GraphQLErrorWithHTTPCode(code=403, message=f"You can delete only your own todo items")

        if description:
            new_data.update({"description": description})
        if date:
            in_date_format = datetime.date.fromisoformat(date)
            new_data.update({"date": in_date_format})

        # Check if exist new data to update current todo_item, otherwise returns current object with origin data.
        if not new_data:
            return {
                "todo": current_object
            }

        response = await todo_crud_service.update(
            session,
            obj_current=current_object,
            **new_data
        )

    return {
        "todo": response
    }


@convert_kwargs_to_snake_case
async def resolve_create_user(obj, info, email, password):
    hashed_password = get_password_hash(password)
    async with manage_session() as session:
        try:
            created_user = await user_crud_service.create(
                session=session, email=email, hashed_password=hashed_password
            )
            print(created_user.id, created_user.email, created_user.todos)
            return {
                "user": created_user
            }
        except IntegrityError:
            await session.rollback()
            raise GraphQLErrorWithHTTPCode(code=422, message=f"The user is already exist.")


@convert_kwargs_to_snake_case
async def resolve_login(obj, info, email, password):
    async with manage_session() as session:
        user = await user_crud_service.authenticate(session=session, email=email, password=password)
        if not user:
            raise GraphQLErrorWithHTTPCode(code=404, message=f"Incorrect email or password")

    access_token_expire = datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(user.id, expires_delta=access_token_expire)

    return {
        "token": access_token,
        "token_type": "bearer"
    }


mutation = MutationType()
mutation.set_field("createTodo", resolve_create_todo_item)
mutation.set_field("deleteTodo", resolve_delete_todo_item)
mutation.set_field("markDone", resolve_mark_done_todo_item)
mutation.set_field("updateTodo", resolve_update_todo_item)
mutation.set_field("createUser", resolve_create_user)
mutation.set_field("createToken", resolve_login)
