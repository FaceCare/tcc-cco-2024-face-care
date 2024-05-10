from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import Query, Body
from typing import List

from schema.user_schema import (GetUsersSchema, UserCreateSchema)
from service.user_service import UserService
from config.get_db import get_db

app_router = APIRouter()

@app_router.post('/', status_code=201)
def post(
    db: Session = Depends(get_db),
    user: UserCreateSchema=Body()
    ):
    
    UserService.create_user(db, user)

@app_router.get('/', status_code=200,
                response_model=List[GetUsersSchema])
def get(
    db: Session = Depends(get_db),
    limit: int=Query(default=100)
    ) -> List[GetUsersSchema]:
    
    return UserService.get_users(db, limit)
