from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..crud import user as user_crud
from ..schemas import User, UserCreate, UserUpdate
from ..database import get_db
from ..utils.security import get_current_active_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=User, summary="Criar novo usuário",
    description="Este endpoint cria um novo usuário no sistema. O e-mail fornecido será verificado para garantir que não há um usuário com o mesmo e-mail já registrado.",
    responses={
        201: {
            "description": "Usuário criado com sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "email": "user@example.com",
                        "full_name": "John Doe",
                        "is_active": True,
                    }
                }
            }
        },
        400: {
            "description": "E-mail já registrado",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Email already registered"
                    }
                }
            }
        }
    })
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_crud.create_user(db=db, user=user)

@router.get("/me", response_model=User,  summary="Obter informações do usuário logado",
    description="Este endpoint retorna as informações do usuário atualmente autenticado. Requer autenticação para acessar.",
    responses={
        200: {
            "description": "Informações do usuário logado",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "email": "user@example.com",
                        "full_name": "John Doe",
                        "is_active": True,
                    }
                }
            }
        },
        401: {
            "description": "Usuário não autenticado",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Not authenticated"
                    }
                }
            }
        }
    })
def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@router.patch("/me", response_model=User, summary="Atualizar informações do usuário",
    description="Atualiza informações do usuário logado. Campos opcionais: nome, email, senha.",
    responses={
        200: {
            "description": "Informações atualizadas com sucesso",
            "content": {"application/json": {"example": {"id": 1, "email": "novo@email.com", "name": "Novo Nome", "is_active": True}}}
        },
        400: {
            "description": "Email já registrado ou dados inválidos",
            "content": {"application/json": {"example": {"detail": "Email already registered"}}}
        },
        401: {
            "description": "Não autenticado",
            "content": {"application/json": {"example": {"detail": "Not authenticated"}}}
        }
    })
def update_user_me(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    if user_update.email and user_update.email != current_user.email:
        db_user = user_crud.get_user_by_email(db, email=user_update.email)
        if db_user:
            raise HTTPException(status_code=400, detail="Email already registered")
    
    return user_crud.update_user(db, user_id=current_user.id, user=user_update)


@router.delete("/me", response_model=User, summary="Deletar usuário logado",
    description="Remove permanentemente a conta do usuário autenticado.",
    responses={
        200: {
            "description": "Usuário deletado com sucesso",
            "content": {"application/json": {"example": {"id": 1, "email": "user@example.com", "name": "John Doe", "is_active": True}}}
        },
        401: {
            "description": "Não autenticado",
            "content": {"application/json": {"example": {"detail": "Not authenticated"}}}
        }
    })
def delete_user_me(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return user_crud.delete_user(db, user_id=current_user.id)