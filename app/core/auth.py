from jose import jwt
from fastapi.security import utils
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.database import schema
from app.services.user import user_crud_service
from app.errors import GraphQLErrorWithHTTPCode


async def get_current_user(info, session: AsyncSession) -> schema.User:
    """
    Get current user by validate access-token from info param.
    """
    # get list of value of authorization header
    auth_header_list = [header[1] for header in info.context["request"]["headers"] if header[0] == b'authorization']

    if not auth_header_list:
        raise GraphQLErrorWithHTTPCode(code=400, message="Bad request, the Authorization header not found.")
    # Get
    auth_header = auth_header_list[0].decode()

    _, access_token = utils.get_authorization_scheme_param(auth_header)

    try:
        payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = int(payload["sub"])
    except jwt.JWTError:
        raise GraphQLErrorWithHTTPCode(code=403, message="Could not validate credentials")

    user = await user_crud_service.get_by_id(session=session, id=user_id)

    if not user:
        raise GraphQLErrorWithHTTPCode(code=404, message="User not found")
    return user
