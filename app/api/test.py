from fastapi import APIRouter
from sqlmodel import select

from app.api.util import DbSession
from app.services.database.models import User

test_router = APIRouter(tags=["test"])


@test_router.get("/test1")
async def test1(session: DbSession):
    # settings_service = get_service(ServiceType.SETTINGS_SERVICE)
    # return settings_service.settings
    stmt = select(User)
    result = await session.execute(stmt)
    return result.scalars().all()
