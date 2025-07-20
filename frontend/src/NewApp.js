import React, { useState, useEffect, createContext, useContext } from 'react';
import axios from 'axios';
import ModernDashboard from './ModernApp';
import './App.css';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Context for authentication
const AuthContext = createContext();

const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};

// Authentication Provider Component
const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const checkAuth = async () => {
      if (token) {
        try {
          const response = await axios.get(`${API}/users/me`, {
            headers: { Authorization: `Bearer ${token}` }
          });
          setUser(response.data);
        } catch (error) {
          localStorage.removeItem('token');
          setToken(null);
        }
      }
      setLoading(false);
    };

    checkAuth();
  }, [token]);

  const login = (userData, userToken) => {
    setUser(userData);
    setToken(userToken);
    localStorage.setItem('token', userToken);
  };

  const logout = () => {
    setUser(null);
    setToken(null);
    localStorage.removeItem('token');
  };

  return (
    <AuthContext.Provider value={{ user, token, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
};

// Login Component with Demo Mode
const LoginRegister = () => {
  const [isLogin, setIsLogin] = useState(true);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    department: 'CSE',
    year: 1,
    roll_number: ''
  });
  const [verificationStep, setVerificationStep] = useState(false);
  const [verificationCode, setVerificationCode] = useState('');
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [demoMode, setDemoMode] = useState(false);
  const { login } = useAuth();

  const departments = ['CSE', 'ECE', 'MECH', 'CIVIL', 'EEE', 'AIDS', 'AIML', 'IT', 'CHEMICAL'];

  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const fillDemoData = () => {
    setFormData({
      name: 'Demo Student',
      email: '953624104113@ritrjpm.ac.in',
      password: 'demo123',
      department: 'CSE',
      year: 3,
      roll_number: '953624104113'
    });
    setDemoMode(true);
    setMessage('✨ Demo data filled! You can now login or register.');
  };

  const quickDemoLogin = async () => {
    setLoading(true);
    try {
      const response = await axios.post(`${API}/auth/login`, {
        email: '953624104113@ritrjpm.ac.in',
        password: 'demo123'
      });
      
      localStorage.setItem('token', response.data.access_token);
      localStorage.setItem('user', JSON.stringify(response.data.user));
      login(response.data.user, response.data.access_token);
      setMessage('🎉 Demo login successful!');
    } catch (error) {
      setMessage('❌ Demo user not found. Please use "Demo Mode - Auto Fill" first and register.');
    }
    setLoading(false);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage('');

    try {
      if (isLogin) {
        const response = await axios.post(`${API}/auth/login`, {
          email: formData.email,
          password: formData.password
        });
        
        localStorage.setItem('token', response.data.access_token);
        localStorage.setItem('user', JSON.stringify(response.data.user));
        login(response.data.user, response.data.access_token);
      } else {
        const response = await axios.post(`${API}/auth/register`, formData);
        setMessage(response.data.message);
        
        if (response.data.demo_verification_code) {
          setVerificationCode(response.data.demo_verification_code);
          setMessage(`Registration successful! ${demoMode ? `Demo verification code: ${response.data.demo_verification_code}` : 'Please check your email for verification code.'}`);
        }
        
        setVerificationStep(true);
      }
    } catch (error) {
      setMessage(error.response?.data?.detail || 'An error occurred. Please try again.');
    }
    
    setLoading(false);
  };

  const handleVerification = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      await axios.post(`${API}/auth/verify-email`, {
        email: formData.email,
        verification_code: verificationCode
      });
      
      setMessage('✅ Email verified successfully! You can now login.');
      setVerificationStep(false);
      setIsLogin(true);
    } catch (error) {
      setMessage(error.response?.data?.detail || 'Verification failed. Please try again.');
    }
    
    setLoading(false);
  };

  // Verification Step UI
  if (verificationStep) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-50 via-blue-50 to-pink-50 flex items-center justify-center p-4">
        <div className="max-w-md w-full bg-white rounded-2xl shadow-xl p-8">
          <div className="text-center mb-8">
            <div className="w-16 h-16 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-white text-2xl">📧</span>
            </div>
            <h2 className="text-2xl font-bold text-gray-900 mb-2">Verify Your Email</h2>
            <p className="text-gray-600">Enter the verification code sent to your email</p>
          </div>

          <form onSubmit={handleVerification} className="space-y-6">
            <div>
              <input
                type="text"
                value={verificationCode}
                onChange={(e) => setVerificationCode(e.target.value)}
                placeholder="Enter 6-digit verification code"
                className="w-full px-4 py-3 border border-gray-300 rounded-xl text-center text-lg font-mono tracking-widest focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                maxLength="6"
                required
              />
            </div>

            {message && (
              <div className={`p-4 rounded-lg ${message.includes('success') || message.includes('Demo') ? 'bg-green-50 text-green-700' : 'bg-red-50 text-red-700'}`}>
                {message}
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white font-semibold py-3 px-4 rounded-xl transition-all disabled:opacity-50 shadow-lg hover:shadow-xl"
            >
              {loading ? '⏳ Verifying...' : '✅ Verify Email'}
            </button>

            <button
              type="button"
              onClick={() => {
                setVerificationStep(false);
                setMessage('');
                setVerificationCode('');
              }}
              className="w-full bg-gray-200 hover:bg-gray-300 text-gray-700 font-semibold py-3 px-4 rounded-xl transition-colors"
            >
              ← Back to Registration
            </button>
          </form>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-blue-50 to-pink-50 flex items-center justify-center p-4">
      <div className="max-w-md w-full bg-white rounded-2xl shadow-xl p-8">
        <div className="text-center mb-8">
          <div className="w-16 h-16 bg-gradient-to-r from-purple-500 to-pink-500 rounded-xl flex items-center justify-center mx-auto mb-4">
            <span className="text-white font-bold text-2xl">S</span>
          </div>
          <h1 className="text-4xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent mb-2">StudentMedia</h1>
          <p className="text-gray-600">Ramco Institute of Technology</p>
          <p className="text-sm text-gray-500 mt-2">Connect • Share • Learn 🎓</p>
          
          <div className="flex justify-center mt-6">
            <div className="flex bg-gray-100 rounded-xl p-1">
              <button
                onClick={() => {
                  setIsLogin(true);
                  setMessage('');
                }}
                className={`px-6 py-2 rounded-lg font-semibold transition-all ${
                  isLogin 
                    ? 'bg-gradient-to-r from-purple-500 to-pink-500 text-white shadow-lg' 
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                Login
              </button>
              <button
                onClick={() => {
                  setIsLogin(false);
                  setMessage('');
                }}
                className={`px-6 py-2 rounded-lg font-semibold transition-all ${
                  !isLogin 
                    ? 'bg-gradient-to-r from-purple-500 to-pink-500 text-white shadow-lg' 
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                Register
              </button>
            </div>
          </div>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          {!isLogin && (
            <>
              <div>
                <input
                  type="text"
                  name="name"
                  placeholder="Full Name"
                  value={formData.name}
                  onChange={handleInputChange}
                  className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                  required
                />
              </div>
              <div>
                <input
                  type="text"
                  name="roll_number"
                  placeholder="Roll Number (e.g., 953624104113)"
                  value={formData.roll_number}
                  onChange={handleInputChange}
                  className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                  required
                />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <select
                    name="department"
                    value={formData.department}
                    onChange={handleInputChange}
                    className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                    required
                  >
                    {departments.map(dept => (
                      <option key={dept} value={dept}>{dept}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <select
                    name="year"
                    value={formData.year}
                    onChange={handleInputChange}
                    className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                    required
                  >
                    <option value={1}>1st Year</option>
                    <option value={2}>2nd Year</option>
                    <option value={3}>3rd Year</option>
                    <option value={4}>4th Year</option>
                  </select>
                </div>
              </div>
            </>
          )}

          <div>
            <input
              type="email"
              name="email"
              placeholder="College Email (@ritrjpm.ac.in)"
              value={formData.email}
              onChange={handleInputChange}
              className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              required
            />
          </div>

          <div>
            <input
              type="password"
              name="password"
              placeholder="Password"
              value={formData.password}
              onChange={handleInputChange}
              className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              required
            />
          </div>

          {message && (
            <div className={`p-4 rounded-lg ${message.includes('success') || message.includes('cleared') || message.includes('Demo') ? 'bg-green-50 text-green-700' : 'bg-red-50 text-red-700'}`}>
              {message}
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white font-semibold py-3 px-4 rounded-xl transition-all disabled:opacity-50 shadow-lg hover:shadow-xl"
          >
            {loading ? '⏳ Processing...' : (isLogin ? '🚀 Login' : '📝 Register')}
          </button>
          
          <button
            type="button"
            onClick={fillDemoData}
            className="w-full mt-3 bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white font-semibold py-3 px-4 rounded-xl transition-all duration-200 shadow-lg hover:shadow-xl transform hover:scale-105"
          >
            🎯 Demo Mode - Auto Fill Data
          </button>
          
          <button
            type="button"
            onClick={quickDemoLogin}
            disabled={loading}
            className="w-full mt-2 bg-gradient-to-r from-green-500 to-blue-500 hover:from-green-600 hover:to-blue-600 text-white font-semibold py-3 px-4 rounded-xl transition-all duration-200 shadow-lg hover:shadow-xl transform hover:scale-105 disabled:opacity-50"
          >
            🚀 Quick Demo Login
          </button>
        </form>

        <div className="mt-6 text-center">
          <div className="bg-gradient-to-r from-purple-50 to-pink-50 border border-purple-200 rounded-xl p-4 mb-4">
            <h3 className="text-sm font-semibold text-purple-700 mb-2">🎯 Demo Mode Instructions</h3>
            <div className="text-xs text-purple-600 space-y-1">
              <p><strong>"Auto Fill Data"</strong> - Fills form with demo student info</p>
              <p><strong>"Quick Demo Login"</strong> - Instantly login with demo account</p>
              <p>Demo account: Demo Student (CSE, 3rd Year)</p>
            </div>
          </div>
          
          <div className="text-sm text-gray-600">
            <p>Exclusive to Ramco Institute of Technology students</p>
            <p className="mt-1">Only @ritrjpm.ac.in emails are allowed</p>
          </div>
          
          <div className="mt-4">
            <label className="flex items-center justify-center gap-2 text-sm">
              <input
                type="checkbox"
                checked={demoMode}
                onChange={(e) => setDemoMode(e.target.checked)}
                className="rounded border-gray-300 text-purple-600 focus:ring-purple-500"
              />
              <span className="text-gray-600">Demo Mode (Auto-fill verification code)</span>
            </label>
          </div>
        </div>
      </div>
    </div>
  );
};

// Main App Component
const AppContent = () => {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-50 via-blue-50 to-pink-50 flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center mx-auto mb-4 animate-spin">
            <span className="text-white font-bold text-2xl">S</span>
          </div>
          <p className="text-gray-600">Loading StudentMedia...</p>
        </div>
      </div>
    );
  }

  return user ? <ModernDashboard /> : <LoginRegister />;
};

const App = () => {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
};

export { useAuth };
export default App;
