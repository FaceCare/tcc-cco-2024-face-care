from sqlalchemy.orm import Session

from service.crud_service import CrudService
from repository.user_repository import UserRepository
from schema.user_schema import UserCreateSchema

class UserService(CrudService):

    def __init__(self) -> None:
        super().__init__()

    def update_by_id(self):
        raise NotImplementedError()
