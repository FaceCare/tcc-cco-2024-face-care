from fastapi import APIRouter, Depends
from fastapi.responses import Response
from sqlalchemy.orm import Session
from fastapi import Query, Body, UploadFile
from typing import List

from schema.photo_schema import (GetPhotosSchema, PhotoCreateSchema)
from model.photo_model import Photo
from service.photo_service import PhotoService
from config.get_db import get_db

app_router = APIRouter()

@app_router.post('/', status_code=201)
def post(
    db: Session = Depends(get_db),
    photo_schema: PhotoCreateSchema=Body()
    ):
    
    PhotoService.create(db, Photo, photo_schema)

@app_router.get('/', status_code=200,
                response_model=List[GetPhotosSchema])
def get(
    db: Session = Depends(get_db),
    limit: int=Query(default=100)
    ) -> List[GetPhotosSchema]:
    
    if result := PhotoService.read(db, Photo, limit):
        return result

    return Response(None, 204)

# @app_router.put('/', status_code=200)
# def put(
#     db: Session = Depends(get_db),
#     id: int = Query(),
#     new_login: LoginUpdateSchema = Body()
#     ):
    
#     PhotoService.update_by_id(db)

@app_router.delete('/', status_code=200)
def delete(
    db: Session = Depends(get_db),
    id: int = Query()
    ):
    
    PhotoService.delete_by_id(db, Photo, id)

@app_router.post('/upload', status_code=200)
def upload(
    photo: UploadFile = Depends(PhotoService.validate_photo),
    db: Session = Depends(get_db)
):
    
    PhotoService.upload()
