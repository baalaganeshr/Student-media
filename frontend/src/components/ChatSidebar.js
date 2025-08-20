import React from 'react';

const ChatSidebar = ({ chats, selectedChat, setSelectedChat }) => {
    return (
        <div className="w-80 h-screen bg-secondary border-l border-border flex flex-col">
            {/* Chat Header */}
            <div className="p-5 border-b border-border">
                <div className="flex items-center justify-between mb-4">
                    <h3 className="text-text-primary text-base font-semibold">PChat</h3>
                    <button className="bg-transparent border-none text-text-secondary cursor-pointer text-base">📹</button>
                </div>

                {/* Search */}
                <div className="bg-accent rounded-full p-2 flex items-center gap-2 border border-border">
                    <span className="text-text-secondary text-sm pl-2">🔍</span>
                    <input
                        type="text"
                        placeholder="Search chats"
                        className="bg-transparent border-none outline-none text-text-primary flex-1 text-xs"
                    />
                </div>
            </div>

            {/* Chat List */}
            <div className="flex-1 overflow-auto py-2 scrollbar">
                {chats.map(chat => (
                    <div
                        key={chat.id}
                        onClick={() => setSelectedChat(chat)}
                        className={`p-3 flex items-center gap-3 cursor-pointer transition-all duration-200 border-l-4
                            ${selectedChat?.id === chat.id ? 'bg-accent border-success' : 'border-transparent hover:bg-highlight'}`}
                    >
                        <div className="relative">
                            <div className="w-10 h-10 bg-accent rounded-full flex items-center justify-center text-base">{chat.avatar}</div>
                            {chat.online && (
                                <div className="absolute bottom-0 right-0 w-3 h-3 bg-success rounded-full border-2 border-secondary" />
                            )}
                        </div>
                        <div className="flex-1 min-w-0">
                            <div className="flex justify-between items-center mb-1">
                                <h4 className="text-text-primary text-sm font-medium truncate">{chat.name}</h4>
                                <span className="text-text-secondary text-xxs">{chat.time}</span>
                            </div>
                            <p className="text-text-secondary text-xs truncate">{chat.lastMessage}</p>
                        </div>
                    </div>
                ))}
            </div>

            {/* Add Friends Button */}
            <div className="p-5">
                <button className="w-full bg-warning text-primary border-none p-3 rounded-full text-sm font-bold cursor-pointer transition-all duration-200">
                    Add Friends
                </button>
            </div>
        </div>
    );
};

export default ChatSidebar;
