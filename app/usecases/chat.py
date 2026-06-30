from app.repositories.chat_messages import ChatMessageRepository
from app.services.openrouter_client import OpenRouterClient
from app.db.models import ChatMessage


class ChatUseCase:
    def __init__(self, chat_repo: ChatMessageRepository, openrouter_client: OpenRouterClient):
        self._chat_repo = chat_repo
        self._openrouter_client = openrouter_client

    async def ask(self, user_id: int, prompt: str, system: str | None, max_history: int, temperature: float) -> str:
        """Запрос к LLM и сохранение истории в БД"""
        # 1. Сборка массива сообщений для OpenRouter
        formatted_messages = []

        if system:
            formatted_messages.append({"role": "system", "content": system})

        if max_history > 0:
            history = await self._chat_repo.get_latest_messages(user_id=user_id, limit=max_history)
            for msg in history:
                formatted_messages.append({"role": msg.role, "content": msg.content})

        formatted_messages.append({"role": "user", "content": prompt})

        # Сохранение запроса пользователя в БД
        await self._chat_repo.add_message(user_id=user_id, role="user", content=prompt)

        # Запрос к API OpenRouter
        answer_text = await self._openrouter_client.send_chat_completion(
            messages=formatted_messages,
            temperature=temperature
        )

        # Сохранение ответа в историю БД
        await self._chat_repo.add_message(user_id=user_id, role="assistant", content=answer_text)

        return answer_text

    async def get_history(self, user_id: int, limit: int = 50) -> list[ChatMessage]:
        """Получение истории переписки"""
        return await self._chat_repo.get_latest_messages(user_id=user_id, limit=limit)

    async def clear_history(self, user_id: int) -> None:
        """Очистка контекста пользователя"""
        await self._chat_repo.delete_all_history(user_id=user_id)
