import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import AsyncSessionLocal
from app.repositories.users import UserRepository
from app.repositories.chat_messages import ChatMessageRepository
from app.services.openrouter_client import OpenRouterClient
from app.usecases.auth import AuthUseCase
from app.usecases.chat import ChatUseCase
from app.core import security


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_db() -> AsyncSession:
    """Асинхронные сессии к БД"""
    async with AsyncSessionLocal() as session:
        yield session

def get_user_repository(session: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepository(session)

def get_chat_repository(session: AsyncSession = Depends(get_db)) -> ChatMessageRepository:
    return ChatMessageRepository(session)

def get_openrouter_client() -> OpenRouterClient:
    return OpenRouterClient()

# UseCases
def get_auth_usecase(repo: UserRepository = Depends(get_user_repository)) -> AuthUseCase:
    return AuthUseCase(repo)

def get_chat_usecase(
    repo: ChatMessageRepository = Depends(get_chat_repository),
    client: OpenRouterClient = Depends(get_openrouter_client)
) -> ChatUseCase:
    return ChatUseCase(repo, client)

# Валидация ID пользователя
async def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    """Декодирует token и возвращает user_id из поля sub"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = security.decode_access_token(token)
        user_id_str: str | None = payload.get("sub")
        if user_id_str is None:
            raise credentials_exception
        return int(user_id_str)
    except (jwt.PyJWTError, ValueError):
        raise credentials_exception
