from fastapi import APIRouter
from sqlmodel import select

from app.api.util import DbSession
from app.services.database.models import User
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlmodel import paginate

test_router = APIRouter(tags=["test"])


@test_router.get("/test1")
async def test1(session: DbSession):
    stmt = select(User)
    result = await session.execute(stmt)
    return result.scalars().all()


@test_router.get("/users", response_model=Page[User])
async def get_users(session: DbSession) -> Page[User]:
    stmt = select(User)
    return await paginate(session, stmt)
