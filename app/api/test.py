from fastapi import APIRouter
from app.deps import DbSession
from app.models.user import User
from sqlmodel import select, col

test_router = APIRouter(tags=["test"])


@test_router.get("/test1")
async def test1(session: DbSession):
    stmt = select(User).order_by(col(User.id).desc())
    result = await session.execute(stmt)
    users = result.scalars().all()
    return [User.model_validate(user) for user in users]
