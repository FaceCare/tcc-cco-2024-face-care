from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from fastapi import Query, Body
from typing import List

from schema.login_schema import (GetLoginsSchema, LoginCreateSchema, LoginUpdateSchema)
from model.login_model import Login
from service.login_service import LoginService
from config.get_db import get_db

app_router = APIRouter()

@app_router.post('/', status_code=201)
def post(
    db: Session = Depends(get_db),
    login_schema: LoginCreateSchema=Body()
    ):
    
    LoginService.create(db, Login, login_schema)

@app_router.get('/', status_code=200,
                response_model=List[GetLoginsSchema])
def get(
    db: Session = Depends(get_db),
    limit: int=Query(default=100)
    ) -> List[GetLoginsSchema]:
    
    if result := LoginService.read(db, Login, limit):
        return result

    return JSONResponse(status_code=204)

@app_router.put('/', status_code=200,
                response_model=List[GetLoginsSchema])
def get(
    db: Session = Depends(get_db),
    id: int = Query(),
    new_login: LoginUpdateSchema = Body()
    ):
    
    LoginService.update_by_id(db, Login, id, new_login)
