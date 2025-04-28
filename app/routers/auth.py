from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import Token
from ..utils.security import authenticate_user, create_access_token
from ..config import settings

router = APIRouter(tags=["authentication"])

@router.post("/token", response_model=Token, summary="Gerar token de acesso", description="Este endpoint permite que um usuário se autentique fornecendo seu nome de usuário e senha. Em caso de sucesso, um token JWT é gerado e retornado para o usuário. O token é utilizado para autenticação nas rotas protegidas da API.", responses={
        200: {
            "description": "Token gerado com sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "access_token": "your_access_token_here",
                        "token_type": "bearer"
                    }
                }
            }
        },
        401: {
            "description": "Credenciais incorretas",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Incorrect email or password"
                    }
                }
            }
        }
    }
)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}