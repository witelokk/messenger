import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import Login from './components/Login';
import Register from './components/Register';
import Home from './components/Chats';
import APIClient from './api';

function App() {
  const api = new APIClient("http://" + process.env.REACT_APP_BACK_URL);

  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      setIsAuthenticated(true);
    }
    setIsLoading(false);
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('token');
    setIsAuthenticated(false);
  };

  if (isLoading) {
    return <div>Loading...</div>;
  }

  return (
    <Router>

      <Routes>
        {isAuthenticated ? (
          <>
            <Route path="/chats/:chatId" element={<Home onLogout={handleLogout} api={api} />} />
            <Route path="/chats" element={<Home onLogout={handleLogout} api={api} />} />
            <Route
              path="*"
              element={<Navigate to="/chats" />}
            />
          </>
        ) : (
          <>
            <Route path="/register" element={<Register api={api} />} />
            <Route path="/login" element={<Login api={api} />} />
            <Route path="*" element={<Navigate to="/login" />} />
          </>
        )
        }
      </Routes>
    </Router>
  );
}

export default App;
