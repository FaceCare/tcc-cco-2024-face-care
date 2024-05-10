from pydantic import BaseModel

class GetLoginsSchema(BaseModel):
    class Config:
        from_attributes = True
        
    login: str
    passwd: str # TODO: remove passwd when finish testing

class LoginCreateSchema(BaseModel):
    login: str
    passwd: str

class LoginUpdateSchema(BaseModel):
    login: str
    passwd: str
    