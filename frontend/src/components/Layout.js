import React from 'react';
import { Outlet } from 'react-router-dom';
import LeftSidebar from './LeftSidebar';

const Layout = ({ user, handleLogout }) => {
    return (
        <div className="flex h-screen bg-primary">
            <LeftSidebar user={user} handleLogout={handleLogout} />
            <div className="ml-60 flex-1 flex">
                <Outlet />
            </div>
        </div>
    );
};

export default Layout;
