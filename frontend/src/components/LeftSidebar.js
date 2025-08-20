import React from 'react';

const LeftSidebar = ({ currentView, setCurrentView }) => {
  const navItems = [
    { id: 'home', icon: '🏠', label: 'Home' },
    { id: 'community', icon: '👥', label: 'Create community' },
    { id: 'profile', icon: '👤', label: 'Profile' },
    { id: 'bookmarks', icon: '🔖', label: 'Bookmarks' },
    { id: 'like', icon: '❤️', label: 'Like' },
    { id: 'your-community', icon: '🌐', label: 'Your Community' },
    { id: 'recently-visited', icon: '🕒', label: 'Recently Visited' },
    { id: 'games', icon: '🎮', label: 'Games' },
    { id: 'mela', icon: '🎪', label: 'Mela' }
  ];

  return (
    <div className="w-60 h-screen bg-secondary border-r border-border p-5 fixed left-0 top-0 overflow-hidden">
      {/* Profile Section */}
      <div className="text-center mb-8">
        <div className="w-16 h-16 bg-success rounded-full mx-auto mb-4 flex items-center justify-center text-2xl shadow-glow-green">
          👨‍💻
        </div>
        <h3 className="text-text-primary text-base font-semibold">Aman Kohli</h3>
        <p className="text-text-secondary text-xs">@amankohli9419</p>
      </div>

      {/* Navigation Menu */}
      <nav>
        {navItems.map(item => (
          <div
            key={item.id}
            onClick={() => setCurrentView(item.id)}
            className={`flex items-center gap-3 p-3 my-1 rounded-lg cursor-pointer transition-all duration-200 text-sm
              ${currentView === item.id ? 'bg-accent text-text-primary' : 'text-text-secondary hover:bg-highlight'}`
            }
          >
            <span className="text-base">{item.icon}</span>
            <span>{item.label}</span>
          </div>
        ))}
      </nav>

      {/* Settings */}
      <div className="absolute bottom-5 left-2 right-2">
        <div className="flex items-center gap-3 p-3 rounded-lg cursor-pointer text-text-secondary text-sm">
          <span className="text-base">⚙️</span>
          <span>Setting & Support</span>
        </div>
      </div>
    </div>
  );
};

export default LeftSidebar;
