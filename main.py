from fastapi import FastAPI
from tasks import add

app = FastAPI()


@app.get("/")
async def root():
    result = add.delay(4, 4)
    return {
        "result": result.get(timeout=1),
    }
