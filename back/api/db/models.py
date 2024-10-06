from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from api.db.settings import Base


class Chat(Base):
    '''Chat model with its attributes.'''
    __tablename__ = "chats"
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime)
    chat_messages = relationship("ChatMessage", back_populates="chat")


class ChatMessage(Base):
    '''ChatMessage model with its attributes.'''
    __tablename__ = "chat_messages"
    id = Column(Integer, primary_key=True, index=True)
    index_order = Column(Integer)
    text = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    chat_id = Column(Integer, ForeignKey("chats.id"))

    chat = relationship("Chat", back_populates="chat_messages")