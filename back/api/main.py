import sys

sys.path.append('..')

from fastapi import FastAPI
from api.db.settings import engine, Base
from api.routers import chat

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(chat.router)