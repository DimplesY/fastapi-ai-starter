from loguru import logger
from multiprocessing import cpu_count


def get_number_of_workers(workers=None):
    if workers == -1 or workers is None:
        workers = (cpu_count() * 2) + 1
    logger.debug(f"Number of workers: {workers}")
    return workers


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:create_app",
        host="0.0.0.0",
        port=8000,
        workers=get_number_of_workers(),
        log_level="error",
        reload=False,
        loop="asyncio",
    )
