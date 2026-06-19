import React from 'react';
import { Menu, LogOut } from 'lucide-react';
import { useAuth } from '../../hooks/useAuth';
import { useNavigate } from 'react-router-dom';

interface TopNavbarProps {
  setMobileMenuOpen: (isOpen: boolean) => void;
}

const TopNavbar: React.FC<TopNavbarProps> = ({ setMobileMenuOpen }) => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="sticky top-0 z-10 flex-shrink-0 flex h-16 bg-white border-b border-gray-200 shadow-sm">
      <button
        type="button"
        className="px-4 border-r border-gray-200 text-gray-500 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-blue-500 lg:hidden"
        onClick={() => setMobileMenuOpen(true)}
      >
        <span className="sr-only">Open sidebar</span>
        <Menu className="h-6 w-6" aria-hidden="true" />
      </button>
      
      <div className="flex-1 px-4 flex justify-between">
        <div className="flex-1 flex items-center lg:hidden">
          <span className="text-xl font-black bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
            SupportBot
          </span>
        </div>
        <div className="hidden lg:flex flex-1"></div>
        <div className="ml-4 flex items-center md:ml-6 space-x-4">
          <div className="hidden sm:flex items-center space-x-3 text-sm">
            <span className="font-medium text-gray-700">{user?.username}</span>
            <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800 capitalize">
              {user?.role}
            </span>
          </div>

          <button
            onClick={handleLogout}
            className="flex items-center p-2 rounded-full text-gray-400 hover:text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-blue-500 transition-colors"
            title="Logout"
          >
            <span className="sr-only">Logout</span>
            <LogOut className="h-5 w-5" aria-hidden="true" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default TopNavbar;
