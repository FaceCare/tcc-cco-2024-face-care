from sqlalchemy import Column, BIGINT, VARCHAR, TEXT

from ..config.database import Base

class Photo(Base):
    __tablename__ = "photo"
    __table_args__ = {"schema": "tcc"} # TODO: add schema to env

    id = Column(BIGINT, primary_key=True)
    url = Column(TEXT)
    classification = Column(VARCHAR)
