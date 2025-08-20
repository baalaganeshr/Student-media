import React, { useState, useEffect } from 'react';
import axios from 'axios';
import LeftSidebar from './LeftSidebar';
import MainFeed from './MainFeed';
import TagsSidebar from './TagsSidebar';
import ChatSidebar from './ChatSidebar';

const Layout = ({ user, handleLogout }) => {
    const [currentView, setCurrentView] = useState('home');
    const [selectedChat, setSelectedChat] = useState(null);
    const [posts, setPosts] = useState([]);
    const [tags, setTags] = useState([]);
    const [chats, setChats] = useState([]);

    useEffect(() => {
        const fetchPosts = async () => {
            try {
                const response = await axios.get('/api/posts');
                setPosts(response.data);
            } catch (error) {
                console.error('Error fetching posts:', error);
            }
        };

        const fetchTags = async () => {
            try {
                const response = await axios.get('/api/tags');
                setTags(response.data);
            } catch (error) {
                console.error('Error fetching tags:', error);
            }
        };

        const fetchChats = async () => {
            try {
                const response = await axios.get('/api/chats');
                setChats(response.data);
            } catch (error) {
                console.error('Error fetching chats:', error);
            }
        };

        fetchPosts();
        fetchTags();
        fetchChats();
    }, []);

    return (
        <div className="flex h-screen bg-primary">
            <LeftSidebar user={user} handleLogout={handleLogout} currentView={currentView} setCurrentView={setCurrentView} />
            <div className="ml-60 flex-1 flex">
                <MainFeed posts={posts} />
                <TagsSidebar tags={tags} />
                <ChatSidebar chats={chats} selectedChat={selectedChat} setSelectedChat={setSelectedChat} />
            </div>
        </div>
    );
};

export default Layout;
