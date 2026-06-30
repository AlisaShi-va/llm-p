from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.chat import ChatRequest, ChatResponse
from app.usecases.chat import ChatUseCase
from app.api.deps import get_chat_usecase, get_current_user_id
from app.core.errors import ExternalServiceError

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("", response_model=ChatResponse)
async def chat_generate(
    payload: ChatRequest,
    current_user_id: int = Depends(get_current_user_id),
    usecase: ChatUseCase = Depends(get_chat_usecase)
):
    try:
        answer = await usecase.ask(
            user_id=current_user_id,
            prompt=payload.prompt,
            system=payload.system,
            max_history=payload.max_history,
            temperature=payload.temperature
        )
        return ChatResponse(answer=answer)
    except ExternalServiceError as e:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=e.message)

@router.get("/history")
async def chat_history(
    current_user_id: int = Depends(get_current_user_id),
    usecase: ChatUseCase = Depends(get_chat_usecase)
):
    # Метод возвращает сырые ORM-модели, маппинг FastAPI
    history = await usecase.get_history(user_id=current_user_id)
    return [
        {"id": msg.id, "role": msg.role, "content": msg.content, "created_at": msg.created_at}
        for msg in history
    ]

@router.delete("/history", status_code=status.HTTP_204_NO_CONTENT)
async def clear_chat_history(
    current_user_id: int = Depends(get_current_user_id),
    usecase: ChatUseCase = Depends(get_chat_usecase)
):
    await usecase.clear_history(user_id=current_user_id)
    return None
