// src/components/MessageList.js
import React, { useEffect } from 'react';

function MessageList({ chat, messages }) {
    return (
        <div className="message-list">
            <h3>Messages</h3>
            <ul>
                {messages.map((message) => (
                    <li key={message.id}>
                        <strong>{message.from_user.id == localStorage.getItem('userId') ? 'You' : message.from_user.username}:</strong> {message.text} <br />
                        <small>{new Date(message.created_at).toLocaleString()}</small>
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default MessageList;
