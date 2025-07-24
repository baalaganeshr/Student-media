import React, { useState } from 'react';

function FigmaStyledApp() {
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [currentPage, setCurrentPage] = useState('dashboard');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [newPost, setNewPost] = useState('');
    const [posts, setPosts] = useState([
        { id: 1, author: 'John Doe', avatar: '👨‍💻', content: 'Study group for CS101 tomorrow at 3PM in Library Room 201', time: '2 hours ago', likes: 15, comments: 3, bookmarked: false },
        { id: 2, author: 'Sarah Smith', avatar: '👩‍🔬', content: 'Anyone have notes from yesterday\'s Physics lecture?', time: '4 hours ago', likes: 8, comments: 5, bookmarked: true },
        { id: 3, author: 'Mike Johnson', avatar: '👨‍🎓', content: 'Great presentation on AI today! Thanks everyone who attended.', time: '1 day ago', likes: 23, comments: 8, bookmarked: false }
    ]);

    // Your exact dark theme color palette
    const darkTheme = {
        primary: '#0f0f0f',
        secondary: '#1a1a1a',
        accent: '#2d2d2d',
        highlight: '#3d3d3d',
        text: '#ffffff',
        textSecondary: '#b0b0b0',
        border: '#404040',
        success: '#00ff88',
        warning: '#ff6b35',
        info: '#00b4d8',
        gradient: 'linear-gradient(135deg, #0f0f0f 0%, #1a1a1a 50%, #2d2d2d 100%)',
        cardGradient: 'linear-gradient(145deg, #1a1a1a 0%, #2d2d2d 100%)',
        shadowDark: '0 8px 32px rgba(0, 0, 0, 0.8)',
        shadowLight: '0 4px 16px rgba(255, 255, 255, 0.1)',
        glowGreen: '0 0 20px rgba(0, 255, 136, 0.3)',
        glowBlue: '0 0 20px rgba(0, 180, 216, 0.3)',
        glowOrange: '0 0 20px rgba(255, 107, 53, 0.3)'
    };

    const handleLogin = () => {
        if (email && password) {
            setIsLoggedIn(true);
            setCurrentPage('dashboard');
        } else {
            alert('Please enter both email and password');
        }
    };

    const handleLogout = () => {
        setIsLoggedIn(false);
        setCurrentPage('dashboard');
        setEmail('');
        setPassword('');
    };

    const handleCreatePost = () => {
        if (newPost.trim()) {
            const post = {
                id: posts.length + 1,
                author: 'You',
                avatar: '🎓',
                content: newPost,
                time: 'now',
                likes: 0,
                comments: 0,
                bookmarked: false
            };
            setPosts([post, ...posts]);
            setNewPost('');
        }
    };

    const toggleLike = (postId) => {
        setPosts(posts.map(post => 
            post.id === postId 
                ? { ...post, likes: post.liked ? post.likes - 1 : post.likes + 1, liked: !post.liked }
                : post
        ));
    };

    const toggleBookmark = (postId) => {
        setPosts(posts.map(post => 
            post.id === postId 
                ? { ...post, bookmarked: !post.bookmarked }
                : post
        ));
    };

    // Modern Figma-style Login Page
    const LoginPage = () => (
        <div style={{
            minHeight: '100vh',
            background: darkTheme.gradient,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            padding: '20px',
            fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif'
        }}>
            <div style={{
                background: darkTheme.cardGradient,
                padding: '48px',
                borderRadius: '24px',
                border: `1px solid ${darkTheme.border}`,
                boxShadow: darkTheme.shadowDark,
                maxWidth: '440px',
                width: '100%',
                textAlign: 'center'
            }}>
                {/* Logo */}
                <div style={{
                    width: '80px',
                    height: '80px',
                    background: darkTheme.success,
                    borderRadius: '20px',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontSize: '32px',
                    margin: '0 auto 24px',
                    boxShadow: darkTheme.glowGreen
                }}>
                    🎓
                </div>

                <h1 style={{
                    color: darkTheme.text,
                    fontSize: '32px',
                    fontWeight: '700',
                    margin: '0 0 8px 0',
                    letterSpacing: '-0.02em'
                }}>
                    Welcome back
                </h1>
                
                <p style={{
                    color: darkTheme.textSecondary,
                    fontSize: '16px',
                    margin: '0 0 32px 0',
                    lineHeight: '1.5'
                }}>
                    Sign in to your StudentMedia account
                </p>

                {/* Email Input */}
                <div style={{ marginBottom: '20px', textAlign: 'left' }}>
                    <label style={{
                        color: darkTheme.text,
                        fontSize: '14px',
                        fontWeight: '500',
                        display: 'block',
                        marginBottom: '8px'
                    }}>
                        Email
                    </label>
                    <input
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        placeholder="Enter your email"
                        style={{
                            width: '100%',
                            padding: '16px',
                            background: darkTheme.accent,
                            border: `2px solid ${darkTheme.border}`,
                            borderRadius: '12px',
                            color: darkTheme.text,
                            fontSize: '16px',
                            outline: 'none',
                            transition: 'all 0.2s ease',
                            fontFamily: 'inherit'
                        }}
                        onFocus={(e) => e.target.style.borderColor = darkTheme.success}
                        onBlur={(e) => e.target.style.borderColor = darkTheme.border}
                    />
                </div>

                {/* Password Input */}
                <div style={{ marginBottom: '32px', textAlign: 'left' }}>
                    <label style={{
                        color: darkTheme.text,
                        fontSize: '14px',
                        fontWeight: '500',
                        display: 'block',
                        marginBottom: '8px'
                    }}>
                        Password
                    </label>
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        placeholder="Enter your password"
                        style={{
                            width: '100%',
                            padding: '16px',
                            background: darkTheme.accent,
                            border: `2px solid ${darkTheme.border}`,
                            borderRadius: '12px',
                            color: darkTheme.text,
                            fontSize: '16px',
                            outline: 'none',
                            transition: 'all 0.2s ease',
                            fontFamily: 'inherit'
                        }}
                        onFocus={(e) => e.target.style.borderColor = darkTheme.success}
                        onBlur={(e) => e.target.style.borderColor = darkTheme.border}
                        onKeyPress={(e) => e.key === 'Enter' && handleLogin()}
                    />
                </div>

                {/* Login Button */}
                <button
                    onClick={handleLogin}
                    style={{
                        width: '100%',
                        padding: '16px',
                        background: darkTheme.success,
                        color: darkTheme.primary,
                        border: 'none',
                        borderRadius: '12px',
                        fontSize: '16px',
                        fontWeight: '600',
                        cursor: 'pointer',
                        transition: 'all 0.2s ease',
                        boxShadow: darkTheme.glowGreen,
                        fontFamily: 'inherit'
                    }}
                    onMouseOver={(e) => e.target.style.transform = 'translateY(-1px)'}
                    onMouseOut={(e) => e.target.style.transform = 'translateY(0)'}
                >
                    Sign In
                </button>

                {/* Forgot Password */}
                <p style={{
                    color: darkTheme.textSecondary,
                    fontSize: '14px',
                    margin: '24px 0 0 0',
                    cursor: 'pointer'
                }}>
                    Forgot your password?
                </p>
            </div>

            {/* Background Elements */}
            <div style={{
                position: 'absolute',
                top: '10%',
                right: '10%',
                width: '200px',
                height: '200px',
                background: `radial-gradient(circle, ${darkTheme.success}20 0%, transparent 70%)`,
                borderRadius: '50%',
                pointerEvents: 'none'
            }} />
            <div style={{
                position: 'absolute',
                bottom: '10%',
                left: '10%',
                width: '150px',
                height: '150px',
                background: `radial-gradient(circle, ${darkTheme.info}20 0%, transparent 70%)`,
                borderRadius: '50%',
                pointerEvents: 'none'
            }} />
        </div>
    );

    // Modern Sidebar Navigation
    const Sidebar = () => (
        <div style={{
            width: '280px',
            height: '100vh',
            background: darkTheme.secondary,
            borderRight: `1px solid ${darkTheme.border}`,
            padding: '24px',
            position: 'fixed',
            left: 0,
            top: 0,
            overflowY: 'auto'
        }}>
            {/* Logo */}
            <div style={{
                display: 'flex',
                alignItems: 'center',
                gap: '12px',
                marginBottom: '32px',
                padding: '12px 0'
            }}>
                <div style={{
                    width: '40px',
                    height: '40px',
                    background: darkTheme.success,
                    borderRadius: '12px',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontSize: '20px',
                    boxShadow: darkTheme.glowGreen
                }}>
                    🎓
                </div>
                <span style={{
                    color: darkTheme.text,
                    fontSize: '20px',
                    fontWeight: '700'
                }}>
                    StudentMedia
                </span>
            </div>

            {/* Navigation Items */}
            {[
                { id: 'dashboard', icon: '🏠', label: 'Dashboard' },
                { id: 'posts', icon: '📝', label: 'Posts' },
                { id: 'groups', icon: '👥', label: 'Study Groups' },
                { id: 'events', icon: '📅', label: 'Events' },
                { id: 'messages', icon: '💬', label: 'Messages' },
                { id: 'profile', icon: '👤', label: 'Profile' }
            ].map(item => (
                <div
                    key={item.id}
                    onClick={() => setCurrentPage(item.id)}
                    style={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: '12px',
                        padding: '12px 16px',
                        borderRadius: '12px',
                        cursor: 'pointer',
                        marginBottom: '4px',
                        background: currentPage === item.id ? darkTheme.accent : 'transparent',
                        border: currentPage === item.id ? `1px solid ${darkTheme.success}` : '1px solid transparent',
                        color: currentPage === item.id ? darkTheme.success : darkTheme.textSecondary,
                        transition: 'all 0.2s ease'
                    }}
                    onMouseOver={(e) => {
                        if (currentPage !== item.id) {
                            e.target.style.background = darkTheme.highlight;
                        }
                    }}
                    onMouseOut={(e) => {
                        if (currentPage !== item.id) {
                            e.target.style.background = 'transparent';
                        }
                    }}
                >
                    <span style={{ fontSize: '18px' }}>{item.icon}</span>
                    <span style={{ fontWeight: '500' }}>{item.label}</span>
                </div>
            ))}

            {/* Logout Button */}
            <div style={{
                position: 'absolute',
                bottom: '24px',
                left: '24px',
                right: '24px'
            }}>
                <button
                    onClick={handleLogout}
                    style={{
                        width: '100%',
                        padding: '12px 16px',
                        background: darkTheme.warning,
                        color: darkTheme.primary,
                        border: 'none',
                        borderRadius: '12px',
                        fontSize: '14px',
                        fontWeight: '600',
                        cursor: 'pointer',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        gap: '8px',
                        boxShadow: darkTheme.glowOrange,
                        transition: 'all 0.2s ease'
                    }}
                >
                    <span>🚪</span>
                    Logout
                </button>
            </div>
        </div>
    );

    // Modern Post Card Component
    const PostCard = ({ post }) => (
        <div style={{
            background: darkTheme.cardGradient,
            borderRadius: '16px',
            border: `1px solid ${darkTheme.border}`,
            padding: '24px',
            marginBottom: '16px',
            boxShadow: darkTheme.shadowLight,
            transition: 'all 0.2s ease'
        }}
        onMouseOver={(e) => e.currentTarget.style.transform = 'translateY(-2px)'}
        onMouseOut={(e) => e.currentTarget.style.transform = 'translateY(0)'}
        >
            {/* Post Header */}
            <div style={{
                display: 'flex',
                alignItems: 'center',
                gap: '12px',
                marginBottom: '16px'
            }}>
                <div style={{
                    width: '44px',
                    height: '44px',
                    background: darkTheme.accent,
                    borderRadius: '12px',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontSize: '20px'
                }}>
                    {post.avatar}
                </div>
                <div style={{ flex: 1 }}>
                    <div style={{
                        color: darkTheme.text,
                        fontWeight: '600',
                        fontSize: '16px',
                        marginBottom: '2px'
                    }}>
                        {post.author}
                    </div>
                    <div style={{
                        color: darkTheme.textSecondary,
                        fontSize: '14px'
                    }}>
                        {post.time}
                    </div>
                </div>
                <div style={{
                    padding: '8px',
                    borderRadius: '8px',
                    cursor: 'pointer',
                    color: darkTheme.textSecondary
                }}>
                    ⋯
                </div>
            </div>

            {/* Post Content */}
            <p style={{
                color: darkTheme.text,
                lineHeight: '1.6',
                margin: '0 0 20px 0',
                fontSize: '15px'
            }}>
                {post.content}
            </p>

            {/* Post Actions */}
            <div style={{
                display: 'flex',
                alignItems: 'center',
                gap: '24px',
                paddingTop: '16px',
                borderTop: `1px solid ${darkTheme.border}`
            }}>
                <button
                    onClick={() => toggleLike(post.id)}
                    style={{
                        background: 'none',
                        border: 'none',
                        color: post.liked ? darkTheme.warning : darkTheme.textSecondary,
                        cursor: 'pointer',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '8px',
                        fontSize: '14px',
                        fontWeight: '500',
                        padding: '8px 12px',
                        borderRadius: '8px',
                        transition: 'all 0.2s ease'
                    }}
                    onMouseOver={(e) => e.target.style.background = darkTheme.highlight}
                    onMouseOut={(e) => e.target.style.background = 'none'}
                >
                    <span>{post.liked ? '❤️' : '🤍'}</span>
                    {post.likes}
                </button>
                
                <button style={{
                    background: 'none',
                    border: 'none',
                    color: darkTheme.textSecondary,
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '8px',
                    fontSize: '14px',
                    fontWeight: '500',
                    padding: '8px 12px',
                    borderRadius: '8px',
                    transition: 'all 0.2s ease'
                }}
                onMouseOver={(e) => e.target.style.background = darkTheme.highlight}
                onMouseOut={(e) => e.target.style.background = 'none'}
                >
                    <span>💬</span>
                    {post.comments}
                </button>

                <button
                    onClick={() => toggleBookmark(post.id)}
                    style={{
                        background: 'none',
                        border: 'none',
                        color: post.bookmarked ? darkTheme.success : darkTheme.textSecondary,
                        cursor: 'pointer',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '8px',
                        fontSize: '14px',
                        fontWeight: '500',
                        padding: '8px 12px',
                        borderRadius: '8px',
                        marginLeft: 'auto',
                        transition: 'all 0.2s ease'
                    }}
                    onMouseOver={(e) => e.target.style.background = darkTheme.highlight}
                    onMouseOut={(e) => e.target.style.background = 'none'}
                >
                    <span>{post.bookmarked ? '🔖' : '📑'}</span>
                </button>
            </div>
        </div>
    );

    // Modern Dashboard with Main Content
    const MainContent = () => (
        <div style={{
            marginLeft: '280px',
            minHeight: '100vh',
            background: darkTheme.primary,
            padding: '24px'
        }}>
            {/* Top Header */}
            <div style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                marginBottom: '32px',
                background: darkTheme.secondary,
                padding: '16px 24px',
                borderRadius: '16px',
                border: `1px solid ${darkTheme.border}`
            }}>
                <div>
                    <h1 style={{
                        color: darkTheme.text,
                        fontSize: '28px',
                        fontWeight: '700',
                        margin: '0 0 4px 0'
                    }}>
                        {currentPage === 'dashboard' ? 'Dashboard' : 
                         currentPage === 'posts' ? 'Posts' :
                         currentPage === 'groups' ? 'Study Groups' :
                         currentPage === 'events' ? 'Events' :
                         currentPage === 'messages' ? 'Messages' :
                         currentPage === 'profile' ? 'Profile' : 'Dashboard'}
                    </h1>
                    <p style={{
                        color: darkTheme.textSecondary,
                        margin: 0,
                        fontSize: '16px'
                    }}>
                        Welcome back! Here's what's happening today.
                    </p>
                </div>
                
                <div style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '12px'
                }}>
                    <button style={{
                        padding: '12px',
                        background: darkTheme.accent,
                        border: `1px solid ${darkTheme.border}`,
                        borderRadius: '12px',
                        color: darkTheme.textSecondary,
                        cursor: 'pointer',
                        fontSize: '18px'
                    }}>
                        🔍
                    </button>
                    <button style={{
                        padding: '12px',
                        background: darkTheme.accent,
                        border: `1px solid ${darkTheme.border}`,
                        borderRadius: '12px',
                        color: darkTheme.textSecondary,
                        cursor: 'pointer',
                        fontSize: '18px'
                    }}>
                        🔔
                    </button>
                </div>
            </div>

            {/* Create Post Card */}
            <div style={{
                background: darkTheme.cardGradient,
                borderRadius: '16px',
                border: `1px solid ${darkTheme.border}`,
                padding: '24px',
                marginBottom: '24px'
            }}>
                <div style={{
                    display: 'flex',
                    gap: '16px',
                    alignItems: 'flex-start'
                }}>
                    <div style={{
                        width: '44px',
                        height: '44px',
                        background: darkTheme.success,
                        borderRadius: '50%',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        fontSize: '20px',
                        boxShadow: darkTheme.glowGreen
                    }}>
                        🎓
                    </div>
                    <div style={{ flex: 1 }}>
                        <textarea
                            value={newPost}
                            onChange={(e) => setNewPost(e.target.value)}
                            placeholder="What's on your mind?"
                            style={{
                                width: '100%',
                                minHeight: '80px',
                                background: darkTheme.accent,
                                border: `2px solid ${darkTheme.border}`,
                                borderRadius: '12px',
                                padding: '16px',
                                color: darkTheme.text,
                                fontSize: '16px',
                                resize: 'vertical',
                                outline: 'none',
                                fontFamily: 'inherit',
                                marginBottom: '16px'
                            }}
                            onFocus={(e) => e.target.style.borderColor = darkTheme.success}
                            onBlur={(e) => e.target.style.borderColor = darkTheme.border}
                        />
                        <div style={{
                            display: 'flex',
                            justifyContent: 'space-between',
                            alignItems: 'center'
                        }}>
                            <div style={{
                                display: 'flex',
                                gap: '12px'
                            }}>
                                <button style={{
                                    padding: '8px 12px',
                                    background: 'none',
                                    border: `1px solid ${darkTheme.border}`,
                                    borderRadius: '8px',
                                    color: darkTheme.textSecondary,
                                    cursor: 'pointer',
                                    fontSize: '14px'
                                }}>
                                    📷 Photo
                                </button>
                                <button style={{
                                    padding: '8px 12px',
                                    background: 'none',
                                    border: `1px solid ${darkTheme.border}`,
                                    borderRadius: '8px',
                                    color: darkTheme.textSecondary,
                                    cursor: 'pointer',
                                    fontSize: '14px'
                                }}>
                                    📊 Poll
                                </button>
                            </div>
                            <button
                                onClick={handleCreatePost}
                                disabled={!newPost.trim()}
                                style={{
                                    padding: '12px 24px',
                                    background: newPost.trim() ? darkTheme.success : darkTheme.accent,
                                    color: newPost.trim() ? darkTheme.primary : darkTheme.textSecondary,
                                    border: 'none',
                                    borderRadius: '12px',
                                    fontSize: '14px',
                                    fontWeight: '600',
                                    cursor: newPost.trim() ? 'pointer' : 'not-allowed',
                                    boxShadow: newPost.trim() ? darkTheme.glowGreen : 'none',
                                    transition: 'all 0.2s ease'
                                }}
                            >
                                Post
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            {/* Posts Feed */}
            <div>
                {posts.map(post => (
                    <PostCard key={post.id} post={post} />
                ))}
            </div>
        </div>
    );

    if (!isLoggedIn) {
        return <LoginPage />;
    }

    return (
        <div style={{
            fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
            background: darkTheme.primary,
            minHeight: '100vh'
        }}>
            <Sidebar />
            <MainContent />
        </div>
    );
}

export default FigmaStyledApp;
