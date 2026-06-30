from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models import ChatMessage


class ChatMessageRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def add_message(self, user_id: int, role: str, content: str) -> ChatMessage:
        """Сохранение сообщения в БД"""
        message = ChatMessage(user_id=user_id, role=role, content=content)
        self._session.add(message)
        await self._session.commit()
        await self._session.refresh(message)
        return message

    async def get_latest_messages(self, user_id: int, limit: int) -> list[ChatMessage]:
        """
        Получение последних сообщений пользователя.
        Возвращение сообщений в хронологическом порядке
        """
        if limit == 0:
            return []

        result = await self._session.execute(
            select(ChatMessage)
            .where(ChatMessage.user_id == user_id)
            .order_by(ChatMessage.created_at.desc())
            .limit(limit)
        )
        # Список от старых к новым
        messages = list(result.scalars().all())
        messages.reverse()
        return messages

    async def delete_all_history(self, user_id: int) -> None:
        """Удаление истории сообщений пользователя"""
        await self._session.execute(
            delete(ChatMessage).where(ChatMessage.user_id == user_id)
        )
        await self._session.commit()
