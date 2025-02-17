from logging import Logger


class APIError(Exception):
    status_code: int = None
    message: str = None

    def __init__(
        self, status_code: int = None, message: str = None, logger: Logger = None
    ):
        super().__init__(message)
        if status_code:
            self.status_code = status_code
        if message:
            self.message = message
        if logger:
            logger.warning(message)


class InvalidContent(APIError):
    status_code = 422

    def __init__(self, logger: Logger):
        super().__init__(
            message="Content data is not valid JSON.",
            logger=logger,
        )
