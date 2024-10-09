import datetime
from sqlalchemy.orm import Session
from api.db.schemas import CreateChatMessageInput
from api.db.models import Chat, ChatMessage


def find_chat_messages_by_chat_id(db: Session, chat_id):
    '''Query to find all chat messages with the given chat_id.'''
    return db.query(ChatMessage).filter(
        ChatMessage.chat_id == chat_id
        ).order_by(ChatMessage.index_order.asc()).all()


def find_chat_message_by_index_order(db: Session, chat_id: int, index_order: int) -> ChatMessage:
    '''Returns a chat message matching the given index order.'''
    return db.query(ChatMessage).filter(
        ChatMessage.index_order == index_order,
        ChatMessage.chat_id == chat_id
    ).first()


def find_chat_message_with_higher_index_orders(db: Session, chat_id: int, index_order: int) -> ChatMessage:
    '''Returns a chat message matching the given index order.'''
    return db.query(ChatMessage).filter(
        ChatMessage.index_order > index_order,
        ChatMessage.chat_id == chat_id
    ).all()


def create_new_chat(db: Session) -> Chat:
    '''Creates a new chat on database.'''
    chat = Chat(
        created_at=datetime.datetime.now(),
        chat_messages=[]
    )
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return chat


def create_new_chat_message(
        db: Session,
        chat_id,
        chat_message_data: CreateChatMessageInput,
        is_user_message: bool = True) -> ChatMessage:
    '''Creates a new chat message on database.'''
    latest_chat_message = db.query(ChatMessage).filter(ChatMessage.chat_id == chat_id).order_by(ChatMessage.index_order.desc()).first()
    new_index_order = 1
    if latest_chat_message:
        new_index_order = latest_chat_message.index_order + 1
    
    current_timestamp = datetime.datetime.now()
    chat_message = ChatMessage(
        text=chat_message_data.text,
        chat_id=chat_id,
        index_order=new_index_order,
        created_at=current_timestamp,
        updated_at=current_timestamp,
        is_user_message=is_user_message
    )
    db.add(chat_message)
    db.commit()
    db.refresh(chat_message)
    return chat_message


def update_existing_chat_message(
        db: Session,
        chat_message: ChatMessage,
        chat_message_data: CreateChatMessageInput) -> ChatMessage:
    '''Updates given chat message with new text.'''
    chat_message.text = chat_message_data.text
    chat_message.updated_at = datetime.datetime.now()
    db.add(chat_message)
    db.commit()
    db.refresh(chat_message)
    return chat_message


def update_next_chat_messages(db: Session, chat_id: int, index_order: int):
    '''Updates next chat messages based on the index order deleted.'''
    chat_messages_to_be_updated = find_chat_message_with_higher_index_orders(db, chat_id, index_order)
    for chat_message in chat_messages_to_be_updated:
        chat_message.index_order -= 1
        db.add(chat_message)
    db.commit()


def delete_existing_chat_message(db: Session, chat_message: ChatMessage):
    '''Delete a chat message from database.'''
    db.delete(chat_message)
    db.commit()