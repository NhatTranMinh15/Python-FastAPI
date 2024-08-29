"""Exception"""

from fastapi import HTTPException, status


class BadRequestException(HTTPException):
    """Bad Request Exception"""

    def __init__(self, detail="Bad request") -> None:
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class UnauthorizedException(HTTPException):
    """Unauthorized Exception"""

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized access"
        )


class ForbiddenException(HTTPException):
    """Forbidden Exception"""

    def __init__(
        self,
        detail="You do not have the necessary permissions to access this resource.",
    ) -> None:
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


class ResourceNotFoundException(HTTPException):
    """Resource Not Found Exception"""

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found"
        )


class ConflictException(HTTPException):
    """Conflict Exception"""

    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_409_CONFLICT, detail="Resource already existed"
        )


class InvalidInputException(HTTPException):
    """Invalid Input Exception"""

    def __init__(self, msg=None):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid input data" if msg is None else msg,
        )
