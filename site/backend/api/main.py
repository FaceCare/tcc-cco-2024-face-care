from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination
from dotenv import load_dotenv

from routes import (user_router)

load_dotenv()

app = FastAPI(
    title=f"Face Care",
    version=f"0.0.0",
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

app.include_router(user_router, tags=["User"])

add_pagination(app)
