from sqlalchemy.orm import Session

from repository.user_repository import UserRepository
from schema.user_schema import UserCreateSchema

class UserService:

    @staticmethod
    def get_users(db: Session, limit: int=100):
        return UserRepository.get_users(db, limit)

    @staticmethod
    def create_user(db: Session, user: UserCreateSchema):
        UserRepository.create_user(db, user)
