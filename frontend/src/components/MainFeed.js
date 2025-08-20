import React, { useState, useEffect } from 'react';
import axios from 'axios';

const MainFeed = ({ posts: initialPosts }) => {
    const [posts, setPosts] = useState(initialPosts);
    const [searchQuery, setSearchQuery] = useState('');

    useEffect(() => {
        setPosts(initialPosts);
    }, [initialPosts]);

    const handleLike = async (postId) => {
        try {
            const response = await axios.post(`/api/posts/${postId}/like`);
            const { liked } = response.data;
            setPosts(posts.map(p =>
                p.id === postId
                    ? { ...p, is_liked: liked, likes_count: p.likes_count + (liked ? 1 : -1) }
                    : p
            ));
        } catch (error) {
            console.error('Error liking post:', error);
        }
    };

    const handleBookmark = async (postId) => {
        try {
            const response = await axios.post(`/api/posts/${postId}/bookmark`);
            const { bookmarked } = response.data;
            setPosts(posts.map(p => p.id === postId ? { ...p, is_bookmarked: bookmarked } : p));
        } catch (error) {
            console.error('Error bookmarking post:', error);
        }
    };

    const handleComment = async (postId, commentText) => {
        if (!commentText.trim()) return;
        try {
            await axios.post(`/api/posts/${postId}/comments`, { content: commentText });
            // For simplicity, we're not updating the comment list here.
            // A more robust solution would re-fetch the post or update the state.
            alert('Comment added successfully!');
        } catch (error) {
            console.error('Error adding comment:', error);
        }
    };

    const handleSearch = async (e) => {
        if (e.key === 'Enter') {
            try {
                const response = await axios.post('/api/search', { query: searchQuery });
                setPosts(response.data);
            } catch (error) {
                console.error('Error searching posts:', error);
            }
        }
    };

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
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                        onKeyPress={handleSearch}
                        className="bg-transparent border-none outline-none text-text-primary flex-1 text-sm"
                    />
                </div>
            </div>

            {/* Posts Feed */}
            <div className="p-5 pt-0">
                {posts.map(post => (
                    <PostItem
                        key={post.id}
                        post={post}
                        onLike={handleLike}
                        onBookmark={handleBookmark}
                        onComment={handleComment}
                    />
                ))}
            </div>
        </div>
    );
};

const PostItem = ({ post, onLike, onBookmark, onComment }) => {
    const [commentText, setCommentText] = useState('');

    const submitComment = (e) => {
        e.preventDefault();
        onComment(post.id, commentText);
        setCommentText('');
    };

    return (
        <div className="bg-gradient-card rounded-2xl p-5 mb-5 border border-border shadow-dark">
            {/* Post Header */}
            <div className="flex items-center mb-4">
                <div className="w-10 h-10 bg-success rounded-full flex items-center justify-center mr-3 text-lg">
                    {post.user && post.user.name ? post.user.name.charAt(0).toUpperCase() : ' G'}
                </div>
                <div className="flex-1">
                    <h4 className="text-text-primary text-sm font-semibold">{post.user ? post.user.name : 'Guest'}</h4>
                    <span className="text-text-secondary text-xs">{new Date(post.created_at).toLocaleString()}</span>
                </div>
                <button
                    onClick={() => onBookmark(post.id)}
                    className="bg-transparent border-none text-text-secondary cursor-pointer text-base"
                >
                    {post.is_bookmarked ? '🔖' : '📌'}
                </button>
            </div>

            {/* Post Content */}
            <p className="text-text-primary leading-relaxed mb-4 text-sm">{post.content}</p>

            {/* Post Image (if exists) */}
            {post.image && (
                <div className="w-full h-48 bg-gradient-to-r from-accent to-highlight rounded-lg mb-4 flex items-center justify-center text-5xl text-text-secondary">🖼️</div>
            )}

            {/* Post Actions */}
            <div className="flex items-center gap-5 pt-4 border-t border-border">
                <button
                    onClick={() => onLike(post.id)}
                    className={`bg-transparent border-none cursor-pointer flex items-center gap-2 text-xs ${post.is_liked ? 'text-success' : 'text-text-secondary'}`}
                >
                    <span className="text-sm">👍</span>
                    {post.likes_count}
                </button>
                <button className="bg-transparent border-none text-text-secondary cursor-pointer flex items-center gap-2 text-xs">
                    <span className="text-sm">💬</span>
                    {post.comments_count}
                </button>
                <button className="bg-transparent border-none text-text-secondary cursor-pointer text-sm">🔄</button>
            </div>

            {/* Comments Section */}
            <div className="mt-4 pt-4 border-t border-border">
                {post.comments && post.comments.map(comment => (
                    <div key={comment.id} className="flex items-start gap-2 mb-2">
                        <div className="w-8 h-8 bg-accent rounded-full flex items-center justify-center text-xs">
                            {comment.user.name.charAt(0).toUpperCase()}
                        </div>
                        <div className="flex-1">
                            <p className="text-text-primary text-xs font-semibold">{comment.user.name}</p>
                            <p className="text-text-secondary text-xs">{comment.content}</p>
                        </div>
                    </div>
                ))}
                <form onSubmit={submitComment} className="flex items-center gap-2 mt-2">
                    <input
                        type="text"
                        value={commentText}
                        onChange={(e) => setCommentText(e.target.value)}
                        placeholder="Add a comment..."
                        className="bg-accent rounded-full p-2 flex-1 border border-border text-text-primary text-xs"
                    />
                    <button type="submit" className="bg-success text-primary rounded-full px-4 py-1 text-xs font-bold">
                        Post
                    </button>
                </form>
            </div>
        </div>
    );
};

export default MainFeed;
