import sys

sys.path.append('..')

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.db.settings import engine, Base
from api.routers import chat

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(chat.router)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
