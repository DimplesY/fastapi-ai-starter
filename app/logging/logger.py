from loguru import logger
import sys
from pathlib import Path


def configure():
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    logger.configure(
        handlers=[
            {
                "sink": sys.stderr,
                "level": "INFO",
                "enqueue": True,
                "backtrace": True,
                "diagnose": True,
            },
            {
                "sink": "logs/app.log",
                "level": "DEBUG",
                "rotation": "100 MB",
                "retention": "30 days",
                "compression": "zip",
                "enqueue": True,
                "backtrace": True,
                "diagnose": True,
                "serialize": True,
            },
            {
                "sink": "logs/error.log",
                "level": "ERROR",
                "rotation": "100 MB",
                "retention": "90 days",
                "compression": "zip",
                "enqueue": True,
                "backtrace": True,
                "diagnose": True,
                "serialize": True,
            },
        ]
    )
