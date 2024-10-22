// src/components/MessageInput.js
import React, { useState } from 'react';

function MessageInput({ toId, onSend }) {
  const [messageText, setMessageText] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!messageText) return;

    // Send the message using the onSend function passed as prop
    await onSend(toId, messageText);
    
    // Clear the input after sending
    setMessageText('');
  };

  return (
    <form onSubmit={handleSubmit} style={{ display: 'flex', marginTop: '20px' }}>
      <input
        type="text"
        value={messageText}
        onChange={(e) => setMessageText(e.target.value)}
        placeholder="Type a message..."
        style={{ flex: 1, padding: '10px', marginRight: '10px' }}
      />
      <button type="submit" style={{ padding: '10px' }}>Send</button>
    </form>
  );
}

export default MessageInput;
