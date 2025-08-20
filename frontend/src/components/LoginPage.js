import React from 'react';

const LoginPage = ({ email, setEmail, password, setPassword, handleLogin }) => {
  return (
    <div className="min-h-screen bg-gradient-primary flex items-center justify-center p-5">
      <div className="bg-gradient-card p-12 rounded-3xl border border-border shadow-dark text-center text-text-primary max-w-md w-full">
        <div className="w-20 h-20 bg-gradient-to-r from-success to-info rounded-full mx-auto mb-5 flex items-center justify-center text-4xl shadow-glow-green shadow-glow-blue">
          🎓
        </div>

        <h1 className="text-5xl mb-2 font-bold bg-gradient-to-r from-success to-info text-transparent bg-clip-text">
          StudentMedia
        </h1>
        <p className="mb-10 text-text-secondary">
          Connect with classmates and build your academic network
        </p>

        <div className="mb-6">
          <input
            type="email"
            placeholder="Enter your email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full p-4 mb-5 rounded-xl border-2 border-border bg-accent text-text-primary text-base outline-none"
          />
          <input
            type="password"
            placeholder="Enter your password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleLogin()}
            className="w-full p-4 mb-6 rounded-xl border-2 border-border bg-accent text-text-primary text-base outline-none"
          />
        </div>

        <button
          onClick={handleLogin}
          className="bg-gradient-to-r from-success to-info text-primary border-none py-4 px-10 rounded-3xl cursor-pointer text-lg font-bold w-full shadow-glow-green shadow-glow-blue"
        >
          🚀 Login to StudentMedia
        </button>
      </div>
    </div>
  );
};

export default LoginPage;
