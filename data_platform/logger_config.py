from loguru import logger

from data_platform.config import settings

LOG_LEVEL = settings.app.LOG_LEVEL
LOG_FOLDER = settings.app.LOG_FOLDER


if LOG_LEVEL in ["DEBUG", "TRACE"]:
    logger.add(f"{LOG_FOLDER}/logs.log", format="{time} {level} {message}",
               level=LOG_LEVEL, rotation="5 MB", backtrace=True, diagnose=True)
else:
    logger.add(f"{LOG_FOLDER}/logs.log", format="{time} {level} {message}", level=LOG_LEVEL, rotation="5 MB")