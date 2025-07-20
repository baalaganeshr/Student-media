import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from './AuthContext';

const API = process.env.REACT_APP_API_URL || 'http://localhost:8001';

const Dashboard = () => {
  const { user, logout } = useAuth();
  const [posts, setPosts] = useState([]);
  const [newPost, setNewPost] = useState('');
  const [selectedImage, setSelectedImage] = useState(null);
  const [loading, setLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [searchDepartment, setSearchDepartment] = useState('');
  const [searchYear, setSearchYear] = useState('');
  const [isSearching, setIsSearching] = useState(false);

  const token = localStorage.getItem('token');
  const departments = ['CSE', 'ECE', 'MECH', 'CIVIL', 'EEE', 'AIDS', 'AIML', 'IT', 'CHEMICAL'];

  useEffect(() => {
    loadPosts();
  }, []);

  const loadPosts = async () => {
    try {
      const response = await axios.get(`${API}/posts`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setPosts(response.data);
    } catch (error) {
      console.error('Error loading posts:', error);
    }
  };

  const handleImageSelect = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => setSelectedImage(e.target.result);
      reader.readAsDataURL(file);
    }
  };

  const handleCreatePost = async (e) => {
    e.preventDefault();
    if (!newPost.trim()) return;

    setLoading(true);
    try {
      await axios.post(`${API}/posts`, {
        content: newPost,
        image: selectedImage
      }, {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      setNewPost('');
      setSelectedImage(null);
      loadPosts();
    } catch (error) {
      console.error('Error creating post:', error);
    }
    setLoading(false);
  };

  const handleSearch = async () => {
    if (!searchQuery.trim() && !searchDepartment && !searchYear) return;
    
    setIsSearching(true);
    try {
      const response = await axios.post(`${API}/posts/search`, {
        query: searchQuery,
        department: searchDepartment,
        year: searchYear ? parseInt(searchYear) : null
      }, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setPosts(response.data);
    } catch (error) {
      console.error('Error searching:', error);
    }
  };

  const handleLike = async (postId) => {
    try {
      await axios.post(`${API}/posts/${postId}/like`, {}, {
        headers: { Authorization: `Bearer ${token}` }
      });
      loadPosts();
    } catch (error) {
      console.error('Error liking post:', error);
    }
  };

  const handleBookmark = async (postId) => {
    try {
      await axios.post(`${API}/posts/${postId}/bookmark`, {}, {
        headers: { Authorization: `Bearer ${token}` }
      });
      loadPosts();
    } catch (error) {
      console.error('Error bookmarking post:', error);
    }
  };

  const formatTimeAgo = (dateString) => {
    const now = new Date();
    const postDate = new Date(dateString);
    const diffInHours = Math.floor((now - postDate) / (1000 * 60 * 60));
    
    if (diffInHours < 1) return 'Just now';
    if (diffInHours < 24) return `${diffInHours}h ago`;
    return `${Math.floor(diffInHours / 24)}d ago`;
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Modern Instagram-style Navigation Header */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-50 shadow-sm">
        <div className="max-w-6xl mx-auto px-4">
          <div className="flex items-center justify-between h-16">
            {/* Logo */}
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-gradient-to-r from-purple-500 to-pink-500 rounded-xl flex items-center justify-center">
                <span className="text-white font-bold text-lg">S</span>
              </div>
              <h1 className="text-2xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
                StudentMedia
              </h1>
            </div>

            {/* Search Bar */}
            <div className="flex-1 max-w-md mx-8">
              <div className="relative">
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="🔍 Search posts, friends, hashtags..."
                  className="w-full bg-gray-100 border-0 rounded-full px-6 py-3 pl-12 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:bg-white transition-all"
                />
                <button
                  onClick={handleSearch}
                  className="absolute right-3 top-1/2 transform -translate-y-1/2 bg-gradient-to-r from-purple-500 to-pink-500 text-white px-4 py-1 rounded-full text-sm hover:shadow-lg transition-all"
                >
                  Search
                </button>
              </div>
            </div>

            {/* User Profile Section */}
            <div className="flex items-center gap-4">
              {/* Notification Bell */}
              <button className="relative p-2 text-gray-600 hover:text-purple-600 transition-colors">
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-3 3 3-3z" />
                </svg>
                <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">3</span>
              </button>
              
              {/* User Profile */}
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full flex items-center justify-center ring-2 ring-purple-200">
                  <span className="text-white font-semibold text-lg">
                    {user?.name?.charAt(0).toUpperCase()}
                  </span>
                </div>
                <div className="hidden md:block">
                  <p className="font-semibold text-gray-900">{user?.name}</p>
                  <p className="text-sm text-gray-500">{user?.department} • {user?.year}th Year</p>
                </div>
                <button
                  onClick={logout}
                  className="ml-2 bg-gradient-to-r from-gray-200 to-gray-300 hover:from-gray-300 hover:to-gray-400 text-gray-700 px-4 py-2 rounded-full transition-all text-sm font-medium"
                >
                  Logout
                </button>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Filter Bar */}
      <div className="bg-white border-b border-gray-100 py-3">
        <div className="max-w-6xl mx-auto px-4">
          <div className="flex items-center gap-4 overflow-x-auto">
            <select
              value={searchDepartment}
              onChange={(e) => setSearchDepartment(e.target.value)}
              className="px-4 py-2 bg-gray-100 border-0 rounded-full text-sm focus:outline-none focus:ring-2 focus:ring-purple-500 min-w-[140px]"
            >
              <option value="">🏢 All Departments</option>
              {departments.map(dept => (
                <option key={dept} value={dept}>{dept}</option>
              ))}
            </select>
            <select
              value={searchYear}
              onChange={(e) => setSearchYear(e.target.value)}
              className="px-4 py-2 bg-gray-100 border-0 rounded-full text-sm focus:outline-none focus:ring-2 focus:ring-purple-500 min-w-[120px]"
            >
              <option value="">📅 All Years</option>
              <option value="1">1st Year</option>
              <option value="2">2nd Year</option>
              <option value="3">3rd Year</option>
              <option value="4">4th Year</option>
            </select>
            {isSearching && (
              <button
                onClick={() => {
                  setSearchQuery('');
                  setSearchDepartment('');
                  setSearchYear('');
                  setIsSearching(false);
                  loadPosts();
                }}
                className="px-4 py-2 bg-red-100 text-red-600 rounded-full text-sm hover:bg-red-200 transition-all font-medium"
              >
                ✕ Clear Filters
              </button>
            )}
          </div>
        </div>
      </div>

      {/* Main Content - Instagram Style Layout */}
      <div className="max-w-6xl mx-auto px-4 py-6">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          
          {/* Left Sidebar - Stories & Quick Actions */}
          <div className="lg:col-span-1 space-y-4">
            {/* Stories Section */}
            <div className="bg-white rounded-xl shadow-sm p-4">
              <h3 className="font-semibold text-gray-900 mb-3">📱 Campus Stories</h3>
              <div className="flex gap-3 overflow-x-auto">
                <div className="flex-shrink-0 text-center">
                  <div className="w-16 h-16 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full flex items-center justify-center ring-4 ring-purple-200 mb-2">
                    <span className="text-white font-bold text-lg">+</span>
                  </div>
                  <p className="text-xs text-gray-600">Your Story</p>
                </div>
                {departments.slice(0, 4).map((dept, index) => (
                  <div key={dept} className="flex-shrink-0 text-center">
                    <div className={`w-16 h-16 bg-gradient-to-r ${
                      index % 3 === 0 ? 'from-pink-500 to-yellow-500' :
                      index % 3 === 1 ? 'from-green-500 to-blue-500' :
                      'from-purple-500 to-pink-500'
                    } rounded-full flex items-center justify-center ring-4 ring-gray-200 mb-2`}>
                      <span className="text-white font-bold text-sm">{dept}</span>
                    </div>
                    <p className="text-xs text-gray-600">{dept}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* Quick Stats */}
            <div className="bg-white rounded-xl shadow-sm p-4">
              <h3 className="font-semibold text-gray-900 mb-3">📊 Your Stats</h3>
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-gray-600">Posts</span>
                  <span className="font-semibold text-purple-600">12</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Followers</span>
                  <span className="font-semibold text-blue-600">234</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Following</span>
                  <span className="font-semibold text-green-600">156</span>
                </div>
              </div>
            </div>
          </div>

          {/* Center - Main Feed */}
          <div className="lg:col-span-2 space-y-6">
            {/* Create Post Card - Instagram Style */}
            <div className="bg-white rounded-xl shadow-sm p-6">
              <div className="flex items-center gap-3 mb-4">
                <div className="w-12 h-12 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full flex items-center justify-center">
                  <span className="text-white font-semibold text-lg">
                    {user?.name?.charAt(0).toUpperCase()}
                  </span>
                </div>
                <div className="flex-1">
                  <textarea
                    value={newPost}
                    onChange={(e) => setNewPost(e.target.value)}
                    placeholder={`What's on your mind, ${user?.name?.split(' ')[0]}? 💭`}
                    className="w-full bg-gray-50 border-0 rounded-lg p-4 resize-none focus:outline-none focus:ring-2 focus:ring-purple-500 transition-all"
                    rows="3"
                  />
                </div>
              </div>
              
              {selectedImage && (
                <div className="mb-4 relative inline-block">
                  <img
                    src={selectedImage}
                    alt="Selected"
                    className="w-full max-w-md h-48 object-cover rounded-xl"
                  />
                  <button
                    type="button"
                    onClick={() => setSelectedImage(null)}
                    className="absolute top-2 right-2 bg-red-500 text-white rounded-full w-8 h-8 flex items-center justify-center text-sm hover:bg-red-600 transition-all"
                  >
                    ✕
                  </button>
                </div>
              )}
              
              <div className="flex items-center justify-between pt-4 border-t border-gray-100">
                <div className="flex items-center gap-4">
                  <input
                    type="file"
                    accept="image/*"
                    onChange={handleImageSelect}
                    className="hidden"
                    id="image-upload"
                  />
                  <label
                    htmlFor="image-upload"
                    className="flex items-center gap-2 text-purple-600 hover:text-purple-700 cursor-pointer font-medium"
                  >
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                    </svg>
                    📷 Photo
                  </label>
                  <button className="flex items-center gap-2 text-green-600 hover:text-green-700 font-medium">
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 4V2a1 1 0 011-1h8a1 1 0 011 1v2m0 0V1a1 1 0 011 1v8a1 1 0 01-1 1H7a1 1 0 01-1-1V3a1 1 0 011-1z"></path>
                    </svg>
                    📍 Location
                  </button>
                </div>
                <button
                  onClick={handleCreatePost}
                  disabled={loading || !newPost.trim()}
                  className="bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white px-8 py-2 rounded-full font-semibold transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-lg hover:shadow-xl"
                >
                  {loading ? '📤 Posting...' : '🚀 Post'}
                </button>
              </div>
            </div>

            {/* Posts Feed */}
            <div className="space-y-6">
              {posts.length === 0 ? (
                <div className="text-center py-16">
                  <div className="w-24 h-24 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center mx-auto mb-4">
                    <span className="text-white text-4xl">📱</span>
                  </div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-2">
                    {isSearching ? 'No posts found' : 'Welcome to StudentMedia!'}
                  </h3>
                  <p className="text-gray-500">
                    {isSearching ? 'Try adjusting your search filters.' : 'Be the first to share something with your college community! 🎓'}
                  </p>
                </div>
              ) : (
                posts.map((post) => (
                  <PostCard
                    key={post.id}
                    post={post}
                    onLike={() => handleLike(post.id)}
                    onBookmark={() => handleBookmark(post.id)}
                    formatTimeAgo={formatTimeAgo}
                    user={user}
                  />
                ))
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// Modern Instagram-style Post Card Component
const PostCard = ({ post, onLike, onBookmark, formatTimeAgo, user }) => {
  const [showComments, setShowComments] = useState(false);
  const [commentText, setCommentText] = useState('');

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
      {/* Post Header */}
      <div className="p-4 pb-3">
        <div className="flex items-center gap-3">
          <div className="w-12 h-12 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-full flex items-center justify-center ring-2 ring-purple-200">
            {post.user.profile_image ? (
              <img src={post.user.profile_image} alt={post.user.name} className="w-12 h-12 rounded-full object-cover" />
            ) : (
              <span className="text-white font-semibold text-lg">
                {post.user.name.charAt(0).toUpperCase()}
              </span>
            )}
          </div>
          <div className="flex-1">
            <div className="flex items-center gap-2">
              <h3 className="font-semibold text-gray-900">{post.user.name}</h3>
              <span className="text-gray-500">•</span>
              <span className="text-sm text-purple-600 font-medium">{post.user.department}</span>
              <span className="text-gray-500">•</span>
              <span className="text-sm text-gray-600">{post.user.year}th Year</span>
            </div>
            <p className="text-sm text-gray-500">{formatTimeAgo(post.created_at)}</p>
          </div>
          <button className="text-gray-400 hover:text-gray-600">
            <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
              <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z"></path>
            </svg>
          </button>
        </div>
      </div>

      {/* Post Content */}
      <div className="px-4 pb-3">
        <p className="text-gray-900 leading-relaxed">{post.content}</p>
      </div>

      {/* Post Image */}
      {post.image && (
        <div className="px-4 pb-3">
          <img 
            src={post.image} 
            alt="Post content" 
            className="w-full h-80 object-cover rounded-xl"
          />
        </div>
      )}

      {/* Action Buttons */}
      <div className="px-4 py-3 border-t border-gray-100">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-6">
            <button 
              onClick={onLike}
              className="flex items-center gap-2 text-gray-600 hover:text-red-500 transition-colors"
            >
              <svg className={`w-6 h-6 ${post.likes?.includes(user?.id) ? 'text-red-500 fill-current' : ''}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path>
              </svg>
              <span className="text-sm font-medium">{post.likes?.length || 0}</span>
            </button>
            
            <button 
              onClick={() => setShowComments(!showComments)}
              className="flex items-center gap-2 text-gray-600 hover:text-blue-500 transition-colors"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
              </svg>
              <span className="text-sm font-medium">{post.comments?.length || 0}</span>
            </button>
            
            <button className="flex items-center gap-2 text-gray-600 hover:text-green-500 transition-colors">
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.367 2.684 3 3 0 00-5.367-2.684z"></path>
              </svg>
            </button>
          </div>
          
          <button 
            onClick={onBookmark}
            className="text-gray-600 hover:text-yellow-500 transition-colors"
          >
            <svg className={`w-6 h-6 ${post.bookmarks?.includes(user?.id) ? 'text-yellow-500 fill-current' : ''}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z"></path>
            </svg>
          </button>
        </div>
      </div>

      {/* Comments Section */}
      {showComments && (
        <div className="px-4 py-3 border-t border-gray-100 bg-gray-50">
          <div className="space-y-3">
            {post.comments?.map((comment, index) => (
              <div key={index} className="flex gap-2">
                <div className="w-8 h-8 bg-gradient-to-r from-blue-400 to-purple-400 rounded-full flex items-center justify-center">
                  <span className="text-white text-xs font-semibold">
                    {comment.author?.charAt(0).toUpperCase()}
                  </span>
                </div>
                <div className="flex-1 bg-white rounded-lg px-3 py-2">
                  <p className="text-sm font-medium text-gray-900">{comment.author}</p>
                  <p className="text-sm text-gray-700">{comment.content}</p>
                </div>
              </div>
            ))}
          </div>
          
          <div className="flex gap-2 mt-3">
            <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full flex items-center justify-center">
              <span className="text-white text-xs font-semibold">
                {user?.name?.charAt(0).toUpperCase()}
              </span>
            </div>
            <div className="flex-1 flex gap-2">
              <input
                type="text"
                value={commentText}
                onChange={(e) => setCommentText(e.target.value)}
                placeholder="Write a comment..."
                className="flex-1 bg-white border border-gray-200 rounded-full px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-purple-500"
              />
              <button 
                onClick={() => {
                  if (commentText.trim()) {
                    setCommentText('');
                  }
                }}
                className="bg-gradient-to-r from-purple-500 to-pink-500 text-white px-4 py-2 rounded-full text-sm font-medium hover:shadow-lg transition-all"
              >
                💬
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;
