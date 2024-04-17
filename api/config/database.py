from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from os import getenv

load_dotenv() # TODO: remove this when add main.py in the root of project

USER_DB = getenv('USER_DB')
PASSWD_DB = getenv('PASSWD_DB')
HOST_BD = getenv('HOST_BD')
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{USER_DB}:{PASSWD_DB}@{HOST_BD}/tcc"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, 
                            autoflush=False, 
                            bind=engine)

Base_Tcc = declarative_base()
