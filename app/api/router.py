from fastapi import APIRouter

from app.api.v1 import test_router

router_v1 = APIRouter(prefix="/v1")
router_v1.include_router(test_router)


router = APIRouter(prefix="/api")

router.include_router(router_v1)
