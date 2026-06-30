from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models import User

class UserRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_email(self, email: str) -> User | None:
        """Получение пользователя по email"""
        result = await self._session.execute(
            select(User).where(User.email == email)
        )
        return result.scalars().first()

    async def get_by_id(self, user_id: int) -> User | None:
        """Получение пользователя по id"""
        result = await self._session.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalars().first()

    async def create(self, email: str, password_hash: str, role: str = "user") -> User:
        """Создание новой записи пользователя в БД"""
        user = User(email=email, password_hash=password_hash, role=role)
        self._session.add(user)
        await self._session.commit()
        await self._session.refresh(user)
        return user
