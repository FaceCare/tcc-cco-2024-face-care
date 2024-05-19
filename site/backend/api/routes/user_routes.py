from fastapi import APIRouter, Depends
from fastapi.responses import Response
from sqlalchemy.orm import Session
from fastapi import Query, Body
from typing import List

from schema.user_schema import (GetUsersSchema, UserCreateSchema, UserUpdateSchema)
from model.user_model import User
from service.user_service import UserService
from config.get_db import get_db

app_router = APIRouter()

@app_router.post('/', status_code=201)
def post(
    db: Session = Depends(get_db),
    user: UserCreateSchema=Body()
    ):
    
    UserService.create(db, User, user)


@app_router.get('/', status_code=200,
                response_model=List[GetUsersSchema])
def get(
    db: Session = Depends(get_db),
    limit: int=Query(default=100)
    ) -> List[GetUsersSchema]:
    
    if result := UserService.read(db, User, limit):
        return result

    return Response(None, 204)

# @app_router.put('/', status_code=200)
# def put(
#     db: Session = Depends(get_db),
#     id: int = Query(),
#     new_login: UserUpdateSchema = Body()
#     ):
    
#     UserService.update_by_id(db)

@app_router.delete('/', status_code=200)
def delete(
    db: Session = Depends(get_db),
    id: int = Query()
    ):
    
    UserService.delete_by_id(db, User, id)
