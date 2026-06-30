from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.auth import RegisterRequest, TokenResponse
from app.schemas.user import UserPublic
from app.usecases.auth import AuthUseCase
from app.api.deps import get_auth_usecase, get_current_user_id
from app.core.errors import ConflictError, UnauthorizedError, NotFoundError

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
async def register(
    payload: RegisterRequest,
    usecase: AuthUseCase = Depends(get_auth_usecase)
):
    try:
        return await usecase.register(email=payload.email, password=payload.password)
    except ConflictError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)

@router.post("/login", response_model=TokenResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    usecase: AuthUseCase = Depends(get_auth_usecase)
):
    try:
        # OAuth2PasswordRequestForm использует поле username, куда Swagger передает email
        token = await usecase.login(email=form_data.username, password=form_data.password)
        return TokenResponse(access_token=token, token_type="bearer")
    except UnauthorizedError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.message)

@router.get("/me", response_model=UserPublic)
async def get_me(
    current_user_id: int = Depends(get_current_user_id),
    usecase: AuthUseCase = Depends(get_auth_usecase)
):
    try:
        return await usecase.get_profile(user_id=current_user_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
