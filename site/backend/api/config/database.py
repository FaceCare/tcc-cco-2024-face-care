from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from os import getenv

SQLALCHEMY_DATABASE_URL = getenv('DATABASE_URL')

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, 
                            autoflush=False, 
                            bind=engine)

Base_Tcc = declarative_base()
