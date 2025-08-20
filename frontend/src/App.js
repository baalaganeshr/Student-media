import React, { useState, useEffect } from 'react';
import axios from 'axios';
import LoginPage from './components/LoginPage';
import Layout from './components/Layout';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [user, setUser] = useState(null);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

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
  };

  return (
    <div>
      {isLoggedIn ? (
        <Layout user={user} handleLogout={handleLogout} />
      ) : (
        <LoginPage
          email={email}
          setEmail={setEmail}
          password={password}
          setPassword={setPassword}
          handleLogin={handleLogin}
        />
      )}
    </div>
  );
}

export default App;
