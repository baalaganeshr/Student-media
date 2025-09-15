import React from 'react';

const RightSidebar = ({ selectedChat }) => {
    if (!selectedChat) {
        return (
            <div className="flex-1 flex items-center justify-center text-text-secondary">
                Select a chat to start messaging
            </div>
        );
    }

    return (
        <div className="flex-1 flex flex-col">
            {/* Chat Header */}
            <div className="p-5 border-b border-border flex items-center justify-between">
                <h3 className="text-text-primary text-base font-semibold">{selectedChat.name}</h3>
                <div className="flex items-center gap-4">
                    <button className="bg-transparent border-none text-text-secondary cursor-pointer text-base">📞</button>
                    <button className="bg-transparent border-none text-text-secondary cursor-pointer text-base">📹</button>
                    <button className="bg-transparent border-none text-text-secondary cursor-pointer text-base">⚙️</button>
                </div>
            </div>

            {/* Messages */}
            <div className="flex-1 p-5 overflow-auto">
                <p className="text-text-primary">Messages for {selectedChat.name} will be here.</p>
            </div>

            {/* Message Input */}
            <div className="p-5 border-t border-border">
                <div className="bg-accent rounded-full p-2 flex items-center gap-2 border border-border">
                    <input
                        type="text"
                        placeholder="Type a message..."
                        className="bg-transparent border-none outline-none text-text-primary flex-1 text-sm"
                    />
                    <button className="bg-success text-primary rounded-full px-4 py-1 text-xs font-bold">
                        Send
                    </button>
                </div>
            </div>
        </div>
    );
};

export default RightSidebar;
