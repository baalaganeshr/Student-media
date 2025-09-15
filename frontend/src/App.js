import React, { useState, useEffect } from 'react';
import { Routes, Route, Navigate, useNavigate } from 'react-router-dom';
import axios from 'axios';
import LoginPage from './components/LoginPage';
import Layout from './components/Layout';
import HomePage from './components/HomePage';
import ChatPage from './components/ChatPage';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [user, setUser] = useState(null);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('token');
    const userData = localStorage.getItem('user');
    if (token && userData) {
      setIsLoggedIn(true);
      setUser(JSON.parse(userData));
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    }
  }, []);

  const handleLogin = async () => {
    if (email && password) {
      try {
        const response = await axios.post('/api/auth/login', { email, password });
        const { access_token, user } = response.data;
        localStorage.setItem('token', access_token);
        localStorage.setItem('user', JSON.stringify(user));
        axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
        setIsLoggedIn(true);
        setUser(user);
        navigate('/');
      } catch (error) {
        alert('Login failed. Please check your credentials.');
        console.error('Login error:', error);
      }
    } else {
      alert('Please enter both email and password');
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    delete axios.defaults.headers.common['Authorization'];
    setIsLoggedIn(false);
    setUser(null);
    navigate('/login');
  };

  return (
    <Routes>
      <Route
        path="/login"
        element={
          isLoggedIn ? (
            <Navigate to="/" />
          ) : (
            <LoginPage
              email={email}
              setEmail={setEmail}
              password={password}
              setPassword={setPassword}
              handleLogin={handleLogin}
            />
          )
        }
      />
      <Route
        path="/*"
        element={
          isLoggedIn ? (
            <Layout user={user} handleLogout={handleLogout} />
          ) : (
            <Navigate to="/login" />
          )
        }
      >
        <Route index element={<HomePage />} />
        <Route path="chat" element={<ChatPage />} />
      </Route>
    </Routes>
  );
}

export default App;
