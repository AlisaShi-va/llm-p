from typing import Optional
from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    prompt: str = Field(
        ...,
        min_length=1,
        description="Текст запроса к модели"
    )
    system: Optional[str] = Field(
        None,
        description="Инструкция для задания контекста модели"
    )
    max_history: int = Field(
        default=10,
        ge=0,
        le=50,
        description="Количество последних сообщений из истории"
    )
    temperature: float = Field(
        default=0.7,
        ge=0.0,
        le=2.0,
        description="Креативность модели"
    )

class ChatResponse(BaseModel):
    answer: str = Field(..., description="Ответ модели")
