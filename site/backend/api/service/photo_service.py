from .crud_service import CrudService

class PhotoService(CrudService):

    def __init__(self) -> None:
        super().__init__()

    def update_by_id(self):
        raise NotImplementedError()
