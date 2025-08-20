import React, { useState } from 'react';
import LeftSidebar from './LeftSidebar';
import MainFeed from './MainFeed';
import TagsSidebar from './TagsSidebar';
import ChatSidebar from './ChatSidebar';

const Layout = () => {
    const [currentView, setCurrentView] = useState('home');
    const [selectedChat, setSelectedChat] = useState(null);

    // Sample data from figma-design.html
    const [posts] = useState([
        {
            id: 1,
            author: 'Raguram S',
            avatar: '👨‍💻',
            content: 'Today was an amazing day! Had a great presentation and learned so much from classmates.',
            image: true,
            time: '2h',
            likes: 23,
            comments: 5
        },
        {
            id: 2,
            author: 'Sarah Wilson',
            avatar: '👩‍🎓',
            content: 'Study group session for tomorrow\'s exam. Who\'s joining?',
            time: '4h',
            likes: 18,
            comments: 12
        }
    ]);

    const [chats] = useState([
        { id: 1, name: 'Shah Rukh Khan', avatar: '🎬', lastMessage: 'Hey, how\'s your project going?', time: '2m', online: true },
        { id: 2, name: 'Kamal Hassan', avatar: '🎭', lastMessage: 'See you tomorrow!', time: '5m', online: false },
        { id: 3, name: 'Anudhka Shetty', avatar: '⭐', lastMessage: 'Thanks for the notes!', time: '1h', online: true },
        { id: 4, name: 'Popo Hegde', avatar: '🌟', lastMessage: 'When is the next class?', time: '3h', online: false },
        { id: 5, name: 'Vijay Sethupathi', avatar: '🎪', lastMessage: 'Great job on the presentation', time: '5h', online: false },
        { id: 6, name: 'Samantha', avatar: '✨', lastMessage: 'Can you share the syllabus?', time: '1d', online: true }
    ]);

    const [tags] = useState([
        { name: 'Trending', count: '2.1k', color: '#ff6b35' },
        { name: 'Events', count: '892', color: '#00b4d8' },
        { name: 'Articles', count: '1.5k', color: '#00ff88' }
    ]);

    return (
        <div className="flex h-screen bg-primary">
            <LeftSidebar currentView={currentView} setCurrentView={setCurrentView} />
            <div className="ml-60 flex-1 flex">
                <MainFeed posts={posts} />
                <TagsSidebar tags={tags} />
                <ChatSidebar chats={chats} selectedChat={selectedChat} setSelectedChat={setSelectedChat} />
            </div>
        </div>
    );
};

export default Layout;
