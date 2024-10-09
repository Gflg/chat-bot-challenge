from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from api.db.actions import (
    create_new_chat,
    create_new_chat_message,
    delete_existing_chat_message,
    find_chat_message_by_index_order,
    find_chat_messages_by_chat_id,
    update_existing_chat_message,
    update_next_chat_messages
)
from api.db.schemas import (
    CreateChatOutput,
    CreateChatMessageInput,
    CreateChatMessageOutput
)
from api.db.settings import get_db
from groq_adapter import GroqAdapter
from sqlalchemy.orm import Session

router = APIRouter(prefix='/api/chats')


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_chat(db: Session = Depends(get_db)) -> CreateChatOutput:
    '''
    Endpoint used to create a new chat.
    '''
    chat = create_new_chat(db)

    return {
        'id': chat.id,
        'created_at': chat.created_at
    }


@router.post("/{chat_id}/chat_messages/", status_code=status.HTTP_201_CREATED)
def create_chat_message(
        chat_id: int,
        chat_message_data: CreateChatMessageInput,
        db: Session = Depends(get_db)) -> List[CreateChatMessageOutput]:
    '''
    Endpoint used to create a new chat message in an existing chat.
    '''
    chat_message = create_new_chat_message(db, chat_id, chat_message_data)

    response = [{
        'id': chat_message.id,
        'chat_id': chat_message.chat_id,
        'text': chat_message.text,
        'is_user_message': chat_message.is_user_message,
        'index_order': chat_message.index_order,
        'created_at': chat_message.created_at,
        'updated_at': chat_message.updated_at,
    }]

    groq_adapter = GroqAdapter()
    answer = groq_adapter.get_response(chat_message.text)
    groq_chat_message = create_new_chat_message(db, chat_id, CreateChatMessageInput(text=answer), False)

    response.append({
        'id': groq_chat_message.id,
        'chat_id': groq_chat_message.chat_id,
        'text': groq_chat_message.text,
        'is_user_message': groq_chat_message.is_user_message,
        'index_order': groq_chat_message.index_order,
        'created_at': groq_chat_message.created_at,
        'updated_at': groq_chat_message.updated_at,
    })
    return response


@router.get("/{chat_id}/chat_messages/", status_code=status.HTTP_200_OK)
def get_chat_messages(
        chat_id: int,
        db: Session = Depends(get_db)) -> List[CreateChatMessageOutput]:
    '''
    Endpoint used to retrieve all chat messages in an existing chat.
    '''
    chat_messages = find_chat_messages_by_chat_id(db, chat_id)

    response = []
    
    for chat_message in chat_messages:
        response.append({
            'id': chat_message.id,
            'chat_id': chat_message.chat_id,
            'text': chat_message.text,
            'is_user_message': chat_message.is_user_message,
            'index_order': chat_message.index_order,
            'created_at': chat_message.created_at,
            'updated_at': chat_message.updated_at,
        })

    return response


@router.put("/{chat_id}/chat_messages/{chat_message_index_order}", status_code=status.HTTP_200_OK)
def update_chat_message(
        chat_id: int,
        chat_message_index_order: int,
        chat_message_data: CreateChatMessageInput,
        db: Session = Depends(get_db)) -> List[CreateChatMessageOutput]:
    '''
    Endpoint used to edit a chat message in an existing chat.
    '''
    chat_message = find_chat_message_by_index_order(db, chat_id, chat_message_index_order)
    if chat_message is None:
        raise HTTPException(status_code=404, detail="Chat message not found")
    
    chat_message = update_existing_chat_message(db, chat_message, chat_message_data)

    response = [{
        'id': chat_message.id,
        'chat_id': chat_message.chat_id,
        'text': chat_message.text,
        'is_user_message': chat_message.is_user_message,
        'index_order': chat_message.index_order,
        'created_at': chat_message.created_at,
        'updated_at': chat_message.updated_at
    }]

    next_chat_message = find_chat_message_by_index_order(db, chat_id, chat_message_index_order+1)
    if next_chat_message is not None:
        if not next_chat_message.is_user_message:
            groq_adapter = GroqAdapter()
            answer = groq_adapter.get_response(chat_message.text)
            
            new_groq_message_data = CreateChatMessageInput(text=answer)
            next_chat_message = update_existing_chat_message(db, next_chat_message, new_groq_message_data)

        response.append({
            'id': next_chat_message.id,
            'chat_id': next_chat_message.chat_id,
            'text': next_chat_message.text,
            'is_user_message': next_chat_message.is_user_message,
            'index_order': next_chat_message.index_order,
            'created_at': next_chat_message.created_at,
            'updated_at': next_chat_message.updated_at
        })
    return response


@router.delete("/{chat_id}/chat_messages/{chat_message_index_order}", status_code=status.HTTP_204_NO_CONTENT)
def delete_chat_message(
        chat_id: int,
        chat_message_index_order: int,
        db: Session = Depends(get_db)) -> None:
    '''
    Endpoint used to delete a new chat message in an existing chat.
    '''
    chat_message = find_chat_message_by_index_order(db, chat_id, chat_message_index_order)
    if chat_message is None:
        raise HTTPException(status_code=404, detail="Chat message not found")
    
    chat_message_index_order_deleted = chat_message.index_order
    chat_message = delete_existing_chat_message(db, chat_message)

    update_next_chat_messages(db, chat_id, chat_message_index_order_deleted)
