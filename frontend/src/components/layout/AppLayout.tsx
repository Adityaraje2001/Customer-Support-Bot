import React, { useState } from 'react';
import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';
import MobileSidebar from './MobileSidebar';
import TopNavbar from './TopNavbar';

const AppLayout: React.FC = () => {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="h-screen flex overflow-hidden bg-gray-50">
      <MobileSidebar isOpen={sidebarOpen} setIsOpen={setSidebarOpen} />
      <Sidebar />
      
      <div className="flex flex-col w-0 flex-1 overflow-hidden lg:pl-64">
        <TopNavbar setMobileMenuOpen={setSidebarOpen} />

        <main className="flex-1 relative z-0 overflow-y-auto focus:outline-none">
          <div className="py-6">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 md:px-8">
              <Outlet />
            </div>
          </div>
        </main>
      </div>
    </div>
  );
};

export default AppLayout;
