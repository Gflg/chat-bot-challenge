import datetime
from typing import List
from pydantic import BaseModel


class CreateChatOutput(BaseModel):
    '''Schema used as response models in POST /api/chats/ endpoints.'''
    id: int
    created_at: datetime.datetime


class CreateChatMessageInput(BaseModel):
    '''Schema used as a request model in chat messages endpoints.'''
    text: str


class CreateChatMessageOutput(BaseModel):
    '''Schema used as a response model in chat messages endpoint.'''
    id: int
    chat_id: int
    text: str
    index_order: int
    is_user_message: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime
