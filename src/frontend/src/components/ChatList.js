// src/components/ChatList.js
import React from 'react';

function ChatList({ chats, onSelectChat }) {
  return (
    <div className="chat-list">
      <h3>Chats</h3>
      <ul>
        {chats.map((chat) => (
          <li key={chat.to_user.id} onClick={() => onSelectChat(chat.to_user.id)}>
            {chat.to_user.username}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default ChatList;
