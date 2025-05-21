from fastapi import FastAPI
from celery_tasks import task_01
app = FastAPI()

@app.get("/")
async def root():
    result = task_01.add.delay(4, 4)
    return {
        "result": result.get(timeout=1),
    }
