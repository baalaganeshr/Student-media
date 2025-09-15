import React from 'react';
import { Link, useLocation } from 'react-router-dom';

const LeftSidebar = ({ user, handleLogout }) => {
  const location = useLocation();

  const navItems = [
    { id: 'home', icon: '🏠', label: 'Home', path: '/' },
    { id: 'chat', icon: '💬', label: 'PChat', path: '/chat' },
    { id: 'community', icon: '👥', label: 'Create community', path: '#' },
    { id: 'profile', icon: '👤', label: 'Profile', path: '#' },
    { id: 'bookmarks', icon: '🔖', label: 'Bookmarks', path: '#' },
    { id: 'like', icon: '❤️', label: 'Like', path: '#' },
    { id: 'your-community', icon: '🌐', label: 'Your Community', path: '#' },
    { id: 'recently-visited', icon: '🕒', label: 'Recently Visited', path: '#' },
    { id: 'games', icon: '🎮', label: 'Games', path: '#' },
    { id: 'mela', icon: '🎪', label: 'Mela', path: '#' }
  ];

  return (
    <div className="w-60 h-screen bg-secondary border-r border-border p-5 fixed left-0 top-0 overflow-hidden">
      {/* Profile Section */}
      <div className="text-center mb-8">
        <div className="w-16 h-16 bg-success rounded-full mx-auto mb-4 flex items-center justify-center text-2xl shadow-glow-green">
          {user && user.name ? user.name.charAt(0).toUpperCase() : '👨‍💻'}
        </div>
        <h3 className="text-text-primary text-base font-semibold">{user ? user.name : 'Guest'}</h3>
        <p className="text-text-secondary text-xs">{user ? `@${user.email.split('@')[0]}`: ''}</p>
      </div>

      {/* Navigation Menu */}
      <nav>
        {navItems.map(item => (
          <Link
            key={item.id}
            to={item.path}
            className={`flex items-center gap-3 p-3 my-1 rounded-lg cursor-pointer transition-all duration-200 text-sm
              ${location.pathname === item.path ? 'bg-accent text-text-primary' : 'text-text-secondary hover:bg-highlight'}`
            }
          >
            <span className="text-base">{item.icon}</span>
            <span>{item.label}</span>
          </Link>
        ))}
      </nav>

      {/* Settings */}
      <div className="absolute bottom-5 left-2 right-2">
        <div
          onClick={handleLogout}
          className="flex items-center gap-3 p-3 rounded-lg cursor-pointer text-text-secondary text-sm hover:bg-highlight"
        >
          <span className="text-base">⚙️</span>
          <span>Logout</span>
        </div>
      </div>
    </div>
  );
};

export default LeftSidebar;
