import React from 'react';

const TagsSidebar = ({ tags }) => {
    return (
        <div className="w-72 h-screen bg-secondary border-l border-border p-5 overflow-auto scrollbar">
            {/* Header */}
            <div className="flex items-center justify-between mb-5">
                <h3 className="text-text-primary text-base font-semibold">Tags</h3>
                <button className="bg-transparent border-none text-text-secondary cursor-pointer text-base">⚙️</button>
            </div>

            {/* Search */}
            <div className="bg-accent rounded-full p-2 flex items-center gap-2 mb-5 border border-border">
                <span className="text-text-secondary text-sm pl-2">🔍</span>
                <input
                    type="text"
                    placeholder="Search"
                    className="bg-transparent border-none outline-none text-text-primary flex-1 text-xs"
                />
            </div>

            {/* Tag Categories */}
            <div className="mb-6">
                <div className="flex gap-2 mb-5">
                    {tags.map(tag => (
                        <div key={tag.name} className="bg-accent p-2 rounded-2xl border border-border cursor-pointer transition-all duration-200">
                            <div className={`text-xs font-semibold`} style={{ color: tag.color }}>{tag.name}</div>
                            <div className="text-text-secondary text-xxs">{tag.count}</div>
                        </div>
                    ))}
                </div>
            </div>

            {/* Recent Activity */}
            <div>
                <h4 className="text-text-primary text-sm font-semibold mb-4">Recent Activity</h4>

                {[
                    { user: 'Shah Rukh Khan', action: 'posted in Computer Science', time: '2h', avatar: '🎬' },
                    { user: 'Anudhka Shetty', action: 'joined Physics Discussion', time: '4h', avatar: '⭐' },
                    { user: 'Dashaa', action: 'shared an article', time: '6h', avatar: '📚' },
                    { user: 'Popo Hegde', action: 'commented on your post', time: '8h', avatar: '🌟' }
                ].map((activity, index) => (
                    <div key={index} className="py-3 border-b border-border last:border-b-0">
                        <div className="flex items-center gap-2">
                            <div className="w-8 h-8 bg-accent rounded-full flex items-center justify-center text-xs">{activity.avatar}</div>
                            <div className="flex-1">
                                <div className="text-text-primary text-xs font-medium">{activity.user}</div>
                                <div className="text-text-secondary text-xxs">{activity.action}</div>
                            </div>
                            <span className="text-text-secondary text-xxs">{activity.time}</span>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default TagsSidebar;
