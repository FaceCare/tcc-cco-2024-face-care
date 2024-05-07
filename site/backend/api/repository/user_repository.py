from sqlalchemy.orm import Session
from typing import List

from model.user_model import User
from schema.user_schema import UserCreateSchema

class UserRepository:

    @staticmethod
    def get_users(db: Session, limit: int=100) -> List[User]:
        return db.query(User).limit(limit).all()

    @staticmethod
    def create_user(db: Session, user: UserCreateSchema):
        new_user = User(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            cpf=user.cpf,
            phone_number=user.phone_number,
            fk_login=user.fk_login,
            fk_photo=user.fk_photo)

        db.add(new_user)
        db.commit()
        db.refresh(new_user)
