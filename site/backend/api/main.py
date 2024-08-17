import logging
import tempfile
import os
import shutil
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from fastapi.exceptions import HTTPException
from datetime import datetime

from integrations.storage_s3 import StorageS3
from enums.bucket_s3_enum import BucketS3Enum
from routes import (user_router, login_router, photo_router, acne_router)

logging.basicConfig(level=logging.INFO)

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    storage_s3 = StorageS3(bucket_name=BucketS3Enum.BUCKET_TRAINED_MODEL.value)
    files_s3 = storage_s3.list_all_files()
    PREFFIX_FOLDER_KERAS = 'last_model_keras'

    def extract_datetime_from_filename(filename):
        try:
            timestamp_str = filename.split(' cnn_model.keras')[0]
            return datetime.strptime(timestamp_str, '%d-%m-%Y %H-%M-%S.%f')
        except ValueError:
            return datetime.min

    if files_s3:
        # Ordenar arquivos pelo timestamp no nome
        files_s3.sort(key=extract_datetime_from_filename, reverse=True)
        last_model_name = os.path.split(files_s3[0])[-1]
    else:
        raise HTTPException(404, 'No model.keras found in bucket...')

    tmp_dir_path = tempfile.gettempdir()
    old_folders = [ item for item in os.listdir(tmp_dir_path) if item.startswith(PREFFIX_FOLDER_KERAS) ]
    for folder in old_folders:
        if os.path.isdir:
            shutil.rmtree(os.path.join(tmp_dir_path, folder))

    tmp_dir = tempfile.mkdtemp(prefix=PREFFIX_FOLDER_KERAS)
    last_model_path = os.path.join(tmp_dir, last_model_name)
    storage_s3.download(last_model_name, last_model_path)

    yield

app = FastAPI(
    title=f"Face Care",
    version=f"1.0.0",
    docs_url="/docs",
    root_path=f"",
    # lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(user_router, tags=["User"], prefix='/user')
app.include_router(login_router, tags=["Login"], prefix='/login')
app.include_router(photo_router, tags=["Photo"], prefix='/photo')
app.include_router(acne_router, tags=["Acne"], prefix='/acne')

add_pagination(app)
