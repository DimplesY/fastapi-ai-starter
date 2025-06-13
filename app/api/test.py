from fastapi import APIRouter

test_router = APIRouter(tags=["test"])


@test_router.get("/test")
def test():
    pass
