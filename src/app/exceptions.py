class ShopException(Exception):
    def __init__(self, message: str) -> None:
        self.message = message

    def __str__(self) -> str:
        return self.message


class RepositoryException(ShopException):
    pass


class UserAlreadyExistsException(RepositoryException):
    pass


class IncorrectCredentialsException(RepositoryException):
    pass


class RefreshTokenNotFoundException(ShopException):
    pass


class ObjectNotFoundException(RepositoryException):
    pass


class ForbiddenException(ShopException):
    pass


class RepositoryException(ShopException):
    pass
