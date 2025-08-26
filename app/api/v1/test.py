from fastapi import APIRouter
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlmodel import apaginate
from sqlmodel import select

from app.api.util import DbSession
from app.services.database.models import User

router = APIRouter(tags=["test"])


@router.get("/test1")
async def test1(session: DbSession):
    stmt = select(User)
    result = await session.exec(stmt)
    return result.all()


@router.get("/users", response_model=Page[User])
async def get_users(session: DbSession) -> Page[User]:
    stmt = select(User)
    return await apaginate(session, stmt)  # type: ignore[arg-type]
