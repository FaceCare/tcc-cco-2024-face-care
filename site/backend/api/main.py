from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination
from dotenv import load_dotenv
import logging

from routes import (user_router, login_router, photo_router, acne_router)

logging.basicConfig(level=logging.INFO)

load_dotenv()

app = FastAPI(
    title=f"Face Care",
    version=f"1.0.0",
    docs_url="/docs",
    root_path=f"",
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
