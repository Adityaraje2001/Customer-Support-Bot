import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

const Navbar: React.FC = () => {
  const { isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <nav className="bg-white/80 backdrop-blur-md sticky top-0 z-50 border-b border-gray-100 shadow-sm">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 justify-between items-center">
          <div className="flex-shrink-0 flex items-center">
            <Link to={isAuthenticated ? '/chat' : '/login'} className="text-2xl font-black bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
              SupportBot
            </Link>
          </div>
          <div className="flex items-center space-x-6">
            {isAuthenticated ? (
              <>
                <Link to="/chat" className="text-blue-600 font-medium transition-colors">
                  Chat
                </Link>
                <Link to="/dashboard" className="text-gray-600 hover:text-blue-600 font-medium transition-colors">
                  Dashboard
                </Link>
                <button
                  onClick={handleLogout}
                  className="rounded-full bg-gray-100 px-5 py-2 text-sm font-semibold text-gray-700 hover:bg-gray-200 hover:shadow-sm transition-all"
                >
                  Logout
                </button>
              </>
            ) : (
              <>
                <Link to="/login" className="text-gray-600 hover:text-blue-600 font-medium transition-colors">
                  Login
                </Link>
                <Link
                  to="/register"
                  className="rounded-full bg-blue-600 px-5 py-2 text-sm font-semibold text-white hover:bg-blue-700 hover:shadow-md transition-all shadow-sm"
                >
                  Register
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
