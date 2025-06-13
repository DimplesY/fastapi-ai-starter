from fastapi import APIRouter

from app.api.test import test_router

router = APIRouter(prefix="/api")

router.include_router(test_router)
