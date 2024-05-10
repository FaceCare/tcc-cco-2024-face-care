from sqlalchemy import Column, BIGINT, VARCHAR, TEXT, DATETIME

from config.database import Base_Tcc

class Photo(Base_Tcc):
    __tablename__ = "photo"

    id = Column(BIGINT, primary_key=True)
    url = Column(TEXT)
    date = Column(DATETIME)
    classification = Column(VARCHAR)
