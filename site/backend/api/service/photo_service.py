import logging
from fastapi import UploadFile
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from .crud_service import CrudService

class PhotoService(CrudService):

    def __init__(self) -> None:
        super().__init__()

    def update_by_id(self):
        raise NotImplementedError()
    
    @staticmethod
    def validate_photo(photo: UploadFile):
        if 'image' not in photo.headers.get('content-type'):
            raise HTTPException(400, 'Just image is allowed on upload photo!')

        return photo

    @staticmethod
    def upload(photo: UploadFile , db: Session):
        logging.info('Uploading photo...')
        
