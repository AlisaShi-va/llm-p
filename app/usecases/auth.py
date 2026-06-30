from app.repositories.users import UserRepository
from app.core import security
from app.core.errors import ConflictError, UnauthorizedError, NotFoundError
from app.db.models import User


class AuthUseCase:
    def __init__(self, user_repo: UserRepository):
        self._user_repo = user_repo

    async def register(self, email: str, password: str) -> User:
        """Регистрация нового пользователя"""
        existing_user = await self._user_repo.get_by_email(email)
        if existing_user:
            raise ConflictError("User with this email already exists")

        password_hash = security.hash_password(password)
        return await self._user_repo.create(email=email, password_hash=password_hash)

    async def login(self, email: str, password: str) -> str:
        """Аутентификация пользователя и выпуск JWT токена"""
        user = await self._user_repo.get_by_email(email)
        if not user or not security.verify_password(password, user.password_hash):
            raise UnauthorizedError("Invalid email or password")

        return security.create_access_token(user_id=user.id, role=user.role)

    async def get_profile(self, user_id: int) -> User:
        """Получение профиля пользователя"""
        user = await self._user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundError("User not found")
        return user
