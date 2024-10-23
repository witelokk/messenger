import React, { useState, useEffect, useRef } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import ChatList from './ChatList';
import MessageList from './MessageList';
import MessageInput from './MessageInput';

function Chats({ onLogout, api }) {
  const { chatId } = useParams();
  const navigate = useNavigate();
  const [selectedChatId, setSelectedChatId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [chats, setChats] = useState({ count: 0, chats: [] });
  const [newChatUsername, setNewChatUsername] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const currentChatIdRef = useRef();
  currentChatIdRef.current = selectedChatId;

  useEffect(() => {
    if (chatId) {
      setSelectedChatId(parseInt(chatId));
    }
  }, [chatId]);

  useEffect(() => {
    const fetchChats = async () => {
      try {
        const chats = await api.getChats();
        setChats(chats);
      } catch (err) {
        setError('Failed to fetch chats');
      }
    };

    fetchChats();
  }, []);

  useEffect(() => {
    if (selectedChatId) {
      const fetchMessages = async () => {
        setLoading(true);
        setError(null);
        try {
          const response = await api.getMessagesTo(selectedChatId);
          setMessages(response.messages);
        } catch (err) {
          setError('Failed to fetch messages');
        } finally {
          setLoading(false);
        }
      };

      fetchMessages();
    }
  }, [selectedChatId]);

  useEffect(() => {
    const token = localStorage.getItem('token');
    const ws = new WebSocket(`ws://${process.env.REACT_APP_BACK_URL}/websocket?token=${token}`);

    ws.onopen = () => {
      console.log('Connected to WebSocket');
      console.log(ws);
    };

    ws.onmessage = (event) => {
      console.log(event.data);
      const data = JSON.parse(event.data);

      const currentChatId = currentChatIdRef.current;

      if (data.event === 'new_message' && (data.new_message.from_id == currentChatId || data.new_message.to_id == currentChatId)) {
        const { new_message } = data;
        setMessages((prevMessages) => [
          ...prevMessages,
          {
            id: new_message.message_id,
            from_id: new_message.from_id,
            to_id: new_message.to_id,
            text: new_message.text,
            created_at: new_message.created_at,
          },
        ]);
      }
    };

    ws.onclose = () => {
      console.log('WebSocket connection closed');
    };

    ws.onerror = (err) => {
      console.error('WebSocket error', err);
    };

    return () => {
      if (ws) {
        ws.close();
      }
    };
  }, []);

  const handleSelectChat = (chatId) => {
    setSelectedChatId(chatId);
    setMessages([]);
    navigate(`/chats/${chatId}`);
  };

  const handleSendMessage = async (toId, text) => {
    try {
      await api.sendMessage(toId, text);
    } catch (err) {
      setError('Failed to send message');
    }
  };

  const handleCreateChat = async () => {
    try {
      const user = await api.getUserByUsername(newChatUsername);

      setChats({
        count: chats.count + 1,
        chats: [...chats.chats, { to_user: user }]
      });

      setSelectedChatId(user.id);
    } catch (e) {
      setError(e.message);
    }
  };

  return (
    <div className="home">
      {localStorage.username}
      <button onClick={onLogout}>Logout</button>
      <div className="chat-container" style={{ display: 'flex' }}>
        <div style={{ width: '30%', borderRight: '1px solid #ccc', padding: '10px' }}>
          <ChatList chats={chats.chats} onSelectChat={handleSelectChat} />

          <div style={{ marginTop: '20px' }}>
            <input
              type="text"
              value={newChatUsername}
              onChange={(e) => setNewChatUsername(e.target.value)}
              placeholder="Enter username to chat"
            />
            <button onClick={handleCreateChat}>Create Chat</button>
          </div>
        </div>

        <div style={{ width: '70%', padding: '10px' }}>
          {loading ? (
            <div>Loading messages...</div>
          ) : error ? (
            <div style={{ color: 'red' }}>Error: {error}</div>
          ) : (selectedChatId && typeof chats.chats.find(c => c.to_user.id == selectedChatId) != "undefined") ? (
            <>
              <MessageList chat={chats.chats.find(c => c.to_user.id == selectedChatId)} messages={messages} />
              {chats.chats.find(c => c.to_user.id == selectedChatId).to_user.active ? (
                <MessageInput toId={selectedChatId} onSend={handleSendMessage} />
              ) : (
                <div>You can't write to this user as they have deleted their account</div>
              )}
            </>
          ) : (
            <div>Select a chat to view messages</div>
          )}
        </div>
      </div>
    </div>
  );
}

export default Chats;
