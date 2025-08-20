import React from 'react';

const MainFeed = ({ posts }) => {
  return (
    <div className="flex-1 h-screen overflow-auto bg-primary scrollbar">
      {/* Header */}
      <div className="bg-secondary p-4 border-b border-border flex items-center justify-between sticky top-0 z-10">
        <div className="flex items-center gap-2">
          <span className="text-xl">👁️</span>
          <h2 className="text-text-primary text-lg font-bold">Student Media</h2>
        </div>
        <div className="flex items-center gap-4">
          <button className="bg-transparent border-none text-text-secondary text-lg cursor-pointer">👥</button>
          <button className="bg-transparent border-none text-text-secondary text-lg cursor-pointer">⚙️</button>
        </div>
      </div>

      {/* Search Bar */}
      <div className="p-5">
        <div className="bg-accent rounded-full p-3 flex items-center gap-2 border border-border">
          <span className="text-text-secondary">🔍</span>
          <input
            type="text"
            placeholder="Search"
            className="bg-transparent border-none outline-none text-text-primary flex-1 text-sm"
          />
        </div>
      </div>

      {/* Posts Feed */}
      <div className="p-5 pt-0">
        {posts.map(post => (
          <div key={post.id} className="bg-gradient-card rounded-2xl p-5 mb-5 border border-border shadow-dark">
            {/* Post Header */}
            <div className="flex items-center mb-4">
              <div className="w-10 h-10 bg-success rounded-full flex items-center justify-center mr-3 text-lg">{post.avatar}</div>
              <div className="flex-1">
                <h4 className="text-text-primary text-sm font-semibold">{post.author}</h4>
                <span className="text-text-secondary text-xs">{post.time}</span>
              </div>
              <button className="bg-transparent border-none text-text-secondary cursor-pointer text-base">⋯</button>
            </div>

            {/* Post Content */}
            <p className="text-text-primary leading-relaxed mb-4 text-sm">{post.content}</p>

            {/* Post Image (if exists) */}
            {post.image && (
              <div className="w-full h-48 bg-gradient-to-r from-accent to-highlight rounded-lg mb-4 flex items-center justify-center text-5xl text-text-secondary">🖼️</div>
            )}

            {/* Post Actions */}
            <div className="flex items-center gap-5 pt-4 border-t border-border">
              <button className="bg-transparent border-none text-text-secondary cursor-pointer flex items-center gap-2 text-xs">
                <span className="text-sm">👍</span>
                {post.likes}
              </button>
              <button className="bg-transparent border-none text-text-secondary cursor-pointer flex items-center gap-2 text-xs">
                <span className="text-sm">💬</span>
                {post.comments}
              </button>
              <button className="bg-transparent border-none text-text-secondary cursor-pointer text-sm">🔄</button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default MainFeed;
