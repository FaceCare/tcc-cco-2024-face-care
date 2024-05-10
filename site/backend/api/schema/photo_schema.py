from pydantic import BaseModel
from datetime import datetime

class GetLoginsSchema(BaseModel):
    class Config:
        from_attributes = True
        
    url: str
    date: datetime
    degree: int

class LoginCreateSchema(BaseModel):
    url: str
    date: datetime
    degree: int
    