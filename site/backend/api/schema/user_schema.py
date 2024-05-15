from pydantic import BaseModel, field_validator, Field

class GetUsersSchema(BaseModel):
    class Config:
        from_attributes = True
        
    first_name: str
    last_name: str
    email: str
    cpf: str
    phone_number: str
    fk_login: int # NOTE: use option join if want to retrieve this fild as a Login table
    fk_photo: int

    @field_validator("cpf")
    def anonymize_cpf(cls, cpf):
        # TODO: anonymize cpf if no needs or remove cpf
        return cpf

class UserCreateSchema(BaseModel):
    first_name: str
    last_name: str
    email: str
    cpf: str
    phone_number: str
    fk_login: int
    fk_photo: int | None = Field(default=None)

class UserUpdateSchema(BaseModel):
    first_name: str
    last_name: str
    email: str
    cpf: str
    phone_number: str
