from sqlalchemy import Column, ForeignKey, BIGINT, VARCHAR

from config.database import Base_Tcc
from model.login_model import Login
from model.photo_model import Photo

class User(Base_Tcc):
    __tablename__ = "user"

    id = Column(BIGINT, primary_key=True)
    first_name = Column(VARCHAR)
    last_name = Column(VARCHAR)
    email = Column(VARCHAR, unique=True)
    cpf = Column(VARCHAR, unique=True)
    phone_number = Column(VARCHAR)

    fk_login = Column(BIGINT, ForeignKey(Login.id))
    fk_photo = Column(BIGINT, ForeignKey(Photo.id))
