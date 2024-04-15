from sqlalchemy import Column, BIGINT, VARCHAR

from ..config.database import Base_Tcc

class Login(Base_Tcc):
    __tablename__ = "login"

    id = Column(BIGINT, primary_key=True)
    login = Column(VARCHAR)
    passwd = Column(VARCHAR)
