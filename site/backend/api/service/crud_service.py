from sqlalchemy.orm import Session
from sqlalchemy import Column
from pydantic import BaseModel
from abc import abstractmethod, ABC

from repository.crud_repository import CrudRepository

class CrudService(ABC):
    
    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def create(db: Session, model: BaseModel, object: BaseModel):
        CrudRepository.create(db, model, **object.__dict__)

    @staticmethod
    def read(db: Session, model: BaseModel, limit: int):
        return CrudRepository.read(db, model, limit)

    @abstractmethod
    def update_by_id(self):
        '''Implement if needed'''
        ...

    @staticmethod
    def delete_by_id(db: Session, model: BaseModel, id: int):
        CrudRepository.delete_by_id(db, model, id)
