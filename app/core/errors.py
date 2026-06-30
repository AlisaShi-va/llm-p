class AppBaseError(Exception):
    """Базовое исключение для приложения"""
    def __init__(self, message: str = "An internal application error occurred"):
        self.message = message
        super().__init__(self.message)

class ConflictError(AppBaseError):
    """Исключение при конфликте данных (дубликат)"""
    pass

class UnauthorizedError(AppBaseError):
    """Исключение при ошибке аутентификации (неверный пароль, отсутствует токен)"""
    pass

class ForbiddenError(AppBaseError):
    """Исключение при нарушении прав доступа"""
    pass

class NotFoundError(AppBaseError):
    """Объект отсутствует"""
    pass

class ExternalServiceError(AppBaseError):
    """Исключение при сбоях во внешних интеграциях"""
    pass
