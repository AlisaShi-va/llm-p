import httpx
from app.core.config import settings
from app.core.errors import ExternalServiceError


class OpenRouterClient:
    def __init__(self):
        self._url = f"{settings.OPENROUTER_BASE_URL.rstrip('/')}/chat/completions"
        self._headers = {
            "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
            "HTTP-Referer": settings.OPENROUTER_REFERER,
            "X-Title": settings.OPENROUTER_TITLE,
            "Content-Type": "application/json"
        }

    async def send_chat_completion(self, messages: list[dict], temperature: float) -> str:
        """Отправка сформированного массива сообщений в OpenRouter"""
        payload = {
            "model": settings.OPENROUTER_MODEL,
            "messages": messages,
            "temperature": temperature
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    self._url,
                    headers=self._headers,
                    json=payload,
                    timeout=45.0
                )

                if response.status_code != 200:
                    raise ExternalServiceError(
                        f"OpenRouter returned status {response.status_code}: {response.text}"
                    )

                data = response.json()
                return data["choices"][0]["message"]["content"]

            except httpx.HTTPError as http_err:
                raise ExternalServiceError(
                    f"Network error occurred while calling OpenRouter: {str(http_err)}"
                )
            except (KeyError, IndexError) as parse_err:
                raise ExternalServiceError(
                    f"Failed to parse OpenRouter response format: {str(parse_err)}"
                )
