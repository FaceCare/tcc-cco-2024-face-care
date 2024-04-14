from sqlalchemy import Column, ForeignKey, Integer, BIGINT, VARCHAR
from sqlalchemy.orm import relationship

from ..config.database import Base
from ..model.login_model import Login
from ..model.photo_model import Photo

class User(Base):
    __tablename__ = "user"
    __table_args__ = {"schema": "tcc"} # TODO: add schema to env

    id = Column(BIGINT, primary_key=True)
    first_name = Column(VARCHAR)
    last_name = Column(VARCHAR)
    email = Column(VARCHAR, unique=True)
    cpf = Column(VARCHAR, unique=True)
    phone_number = Column(VARCHAR)
    fk_login = Column(Integer, ForeignKey(Login.id), primary_key=True)
    fk_photo = Column(Integer, ForeignKey(Photo.id), primary_key=True)
    
    login = relationship('Login', foreign_keys='User.fk_user')
    friend = relationship('User', foreign_keys='User.friend_id')
