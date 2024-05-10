from sqlalchemy.orm import Session
from sqlalchemy import Column
from pydantic import BaseModel

from repository.crud_repository import CrudRepository

class CrudService:
    
    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def create(db: Session, model: BaseModel, object: BaseModel):
        CrudRepository.create(db, model, **object.__dict__)

    @staticmethod
    def read(db: Session, model: BaseModel, limit: int):
        return CrudRepository.read(db, model, limit)

    @staticmethod
    def update_by_id(db: Session, model: BaseModel, id: int, **new_data):
        # FIXXXXXXXXXXXXXX
        CrudRepository.update(db, model, id, new_data)

    @staticmethod
    def delete(db: Session, column: Column, value_delete):
        CrudRepository.delete(db, column, value_delete)
