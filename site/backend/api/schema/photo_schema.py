from pydantic import BaseModel
from datetime import datetime

class GetPhotosSchema(BaseModel):
    class Config:
        from_attributes = True
        
    url: str
    date: datetime
    degree: int

class PhotoCreateSchema(BaseModel):
    url: str
    date: datetime
    degree: int
    