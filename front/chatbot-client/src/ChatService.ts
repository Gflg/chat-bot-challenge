import { Message } from './types';

// Create a new chat and return the chatId
export const createChat = async (): Promise<number> => {
  const response = await fetch('http://localhost:8000/api/chats', { method: 'POST' });
  const data = await response.json();
  return data.id;
};

// Load messages for a given chatId
export const loadMessages = async (chatId: number): Promise<Message[]> => {
  const response = await fetch(`http://localhost:8000/api/chats/${chatId}/chat_messages/`);
  const data = await response.json();
  return data.sort((a: Message, b: Message) => a.index_order - b.index_order);
};

// Send a new message to the chat
export const sendMessage = async (chatId: number, text: string): Promise<void> => {
  await fetch(`http://localhost:8000/api/chats/${chatId}/chat_messages/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text }),
  });
};

// Delete a message from the chat
export const deleteMessage = async (chatId: number, messageId: number): Promise<void> => {
  await fetch(`http://localhost:8000/api/chats/${chatId}/chat_messages/${messageId}`, {
    method: 'DELETE',
  });
};

// Save the edited message
export const saveEditMessage = async (chatId: number, messageId: number, text: string): Promise<void> => {
  await fetch(`http://localhost:8000/api/chats/${chatId}/chat_messages/${messageId}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text }),
  });
};
