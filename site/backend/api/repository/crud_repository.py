from sqlalchemy.orm import Session
from pydantic import BaseModel

class CrudRepository:

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
    def update_by_id(db: Session, model: BaseModel, id: int, **new_data):
        db.query(model).filter_by(model.id == id).update(new_data)
        db.commit()

    @staticmethod
    def delete(db: Session, column, value_delete):
        ...
