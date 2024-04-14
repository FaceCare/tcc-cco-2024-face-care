from sqlalchemy import Column, BIGINT, VARCHAR

from ..config.database import Base

class Login(Base):
    __tablename__ = "login"
    __table_args__ = {"schema": "tcc"} # TODO: add schema to env

    id = Column(BIGINT, primary_key=True)
    login = Column(VARCHAR)
    passwd = Column(VARCHAR)
