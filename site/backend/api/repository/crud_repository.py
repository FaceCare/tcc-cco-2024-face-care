from sqlalchemy.orm import Session
from pydantic import BaseModel
from abc import abstractmethod, ABC

class CrudRepository(ABC):

    @staticmethod
    def create(db: Session, model: BaseModel, **new_data):
        new_object = model(**new_data)
        db.add(new_object)
        db.commit()
        db.refresh(new_object)

    @staticmethod
    def read(db: Session, model: BaseModel, limit: int):
        return db.query(model).limit(limit).all()

    @staticmethod
    @abstractmethod
    def update_by_id(db: Session):
        ...

    @staticmethod
    def delete_by_id(db: Session, model: BaseModel, id: int):
        db.query(model).filter(model.id == id).delete()
        db.commit()
