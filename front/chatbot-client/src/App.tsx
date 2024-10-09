// src/App.tsx
import React, { useEffect, useState } from 'react';
import { createChat, loadMessages, sendMessage, deleteMessage, saveEditMessage } from './ChatService';
import { Message } from './types';

const ChatApp: React.FC = () => {
  const [chatId, setChatId] = useState<number | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [newMessage, setNewMessage] = useState<string>('');
  const [editingMessageId, setEditingMessageId] = useState<number | null>(null);
  const [editingMessageText, setEditingMessageText] = useState<string>('');

  useEffect(() => {
    const initializeChat = async () => {
      const newChatId = await createChat();
      setChatId(newChatId);
      await fetchMessages(newChatId);
    };
    initializeChat();
  }, []);

  const fetchMessages = async (chatId: number) => {
    const messages = await loadMessages(chatId);
    setMessages(messages);
  };

  const handleSendMessage = async () => {
    if (chatId && newMessage.trim() !== '') {
      await sendMessage(chatId, newMessage);
      await fetchMessages(chatId);
      setNewMessage(''); // Clear input
    }
  };

  const handleEditMessage = (messageId: number, oldText: string) => {
    // Set editing state and store the old text
    setEditingMessageId(messageId);
    setEditingMessageText(oldText);
  };

  const handleSaveEdit = async (messageId: number) => {
    if (chatId && editingMessageText.trim() !== '') {
      await saveEditMessage(chatId, messageId, editingMessageText);
      await fetchMessages(chatId); // Reload the messages after saving
      setEditingMessageId(null);   // Exit editing mode
      setEditingMessageText('');   // Clear editing state
    }
  };

  const handleDeleteMessage = async (messageId: number) => {
    if (chatId) {
      await deleteMessage(chatId, messageId);
      await fetchMessages(chatId);
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-header">
        <img src="https://st3.depositphotos.com/8950810/17657/v/450/depositphotos_176577870-stock-illustration-cute-smiling-funny-robot-chat.jpg" alt="Bot Avatar" />
        <h3>Hey👋, I'm Ava</h3>
        <p>Ask me anything or pick a place to start</p>
      </div>

      <div className="chat-body" id="chat-body">
        {messages.map((message) => (
          <div key={message.index_order} className={`chat-message ${message.is_user_message ? 'user' : 'bot'}`} id={`message-${message.index_order}`}>
            {!message.is_user_message && <img src="https://st3.depositphotos.com/8950810/17657/v/450/depositphotos_176577870-stock-illustration-cute-smiling-funny-robot-chat.jpg" alt="Bot Avatar" />}
            <div className={`message-content ${message.is_user_message ? 'user' : 'bot'}`}>
            {editingMessageId === message.index_order ? (
              <>
                {/* Input field and buttons during editing */}
                <input
                  type="text"
                  value={editingMessageText}
                  onChange={(e) => setEditingMessageText(e.target.value)}
                />
                <br></br>
                <button onClick={() => handleSaveEdit(message.index_order)}>Save</button>
                <button onClick={() => setEditingMessageId(null)}>Cancel</button>
              </>
              ) : (
                <>
                  {/* Display message text */}
                  <div>
                    {message.text}
                  </div>
                </>
              )}
            </div>
            <div className="message-controls">
              {editingMessageId !== message.index_order && (
                <>
                  <button className="edit-btn" onClick={() => handleEditMessage(message.index_order, message.text)}>
                    <i className="bi bi-pencil-fill"></i>
                  </button>
                  <button className="delete-btn" onClick={() => handleDeleteMessage(message.index_order)}>
                    <i className="bi bi-trash-fill"></i>
                  </button>
                </>
              )}
            </div>
          </div>
        ))}
      </div>

      <div className="chat-footer">
        <input
          type="text"
          id="user-input"
          value={newMessage}
          onChange={(e) => setNewMessage(e.target.value)}
          placeholder="Your question"
        />
        <button onClick={handleSendMessage}>
          <img src="https://e7.pngegg.com/pngimages/891/367/png-clipart-computer-icons-symbol-send-email-button-miscellaneous-blue.png" alt="Send Icon" />
        </button>
      </div>
    </div>
  );
};

export default ChatApp;
