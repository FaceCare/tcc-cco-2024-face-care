from pydantic import BaseModel

class GetLoginsSchema(BaseModel):
    class Config:
        from_attributes = True
        
    login: str

class LoginCreateSchema(BaseModel):
    login: str
    passwd: str

class LoginUpdateSchema(BaseModel):
    login: str
    passwd: str
    