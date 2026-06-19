import React from 'react';
import { NavLink, useLocation } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import { 
  LayoutDashboard, 
  MessageSquare, 
  Ticket, 
  User, 
  Shield, 
  BarChart,
  X,
  History,
  BookOpen
} from 'lucide-react';

interface MobileSidebarProps {
  isOpen: boolean;
  setIsOpen: (isOpen: boolean) => void;
}

const MobileSidebar: React.FC<MobileSidebarProps> = ({ isOpen, setIsOpen }) => {
  const { user } = useAuth();
  const location = useLocation();

  const navItems = [
    { name: 'Dashboard', path: '/dashboard', icon: LayoutDashboard, roles: ['customer', 'admin'] },
    { name: 'Chat', path: '/chat', icon: MessageSquare, roles: ['customer', 'admin'] },
    { name: 'My Tickets', path: '/my-tickets', icon: Ticket, roles: ['customer', 'admin'] },
    { name: 'Admin Tickets', path: '/admin/tickets', icon: Shield, roles: ['admin'] },
    { name: 'Knowledge Base', path: '/admin/knowledge-base', icon: BookOpen, roles: ['admin'] },
    { name: 'Analytics', path: '/admin/analytics', icon: BarChart, roles: ['admin'] },
    { name: 'Conversations', path: '/conversations', icon: History, roles: ['customer', 'admin'] },
    { name: 'Profile', path: '/profile', icon: User, roles: ['customer', 'admin'] },
  ];

  const filteredItems = navItems.filter(item => 
    user && item.roles.includes(user.role)
  );

  return (
    <>
      {/* Off-canvas menu for mobile */}
      <div className={`relative z-40 lg:hidden ${isOpen ? '' : 'hidden'}`} role="dialog" aria-modal="true">
        {/* Background backdrop */}
        <div 
          className="fixed inset-0 bg-gray-600 bg-opacity-75 transition-opacity" 
          onClick={() => setIsOpen(false)}
        ></div>

        <div className="fixed inset-0 flex z-40">
          <div className="relative flex-1 flex flex-col max-w-xs w-full bg-white transition ease-in-out duration-300 transform">
            <div className="absolute top-0 right-0 -mr-12 pt-2">
              <button
                type="button"
                className="ml-1 flex items-center justify-center h-10 w-10 rounded-full focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white"
                onClick={() => setIsOpen(false)}
              >
                <span className="sr-only">Close sidebar</span>
                <X className="h-6 w-6 text-white" aria-hidden="true" />
              </button>
            </div>

            <div className="flex-1 h-0 pt-5 pb-4 overflow-y-auto">
              <div className="flex-shrink-0 flex items-center px-4">
                <span className="text-2xl font-black bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
                  SupportBot
                </span>
              </div>
              <nav className="mt-8 px-2 space-y-2">
                {filteredItems.map((item) => {
                  const isActive = location.pathname.startsWith(item.path);
                  const Icon = item.icon;
                  return (
                    <NavLink
                      key={item.name}
                      to={item.path}
                      onClick={() => setIsOpen(false)}
                      className={`group flex items-center px-3 py-2.5 text-base font-medium rounded-xl transition-all duration-200 ${
                        isActive
                          ? 'bg-blue-50 text-blue-700 shadow-sm'
                          : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                      }`}
                    >
                      <Icon
                        className={`flex-shrink-0 mr-4 h-6 w-6 transition-colors ${
                          isActive ? 'text-blue-600' : 'text-gray-400 group-hover:text-gray-500'
                        }`}
                        aria-hidden="true"
                      />
                      {item.name}
                    </NavLink>
                  );
                })}
              </nav>
            </div>
            
            <div className="flex-shrink-0 flex border-t border-gray-200 p-4">
              <div className="flex items-center w-full">
                <div className="h-10 w-10 rounded-full bg-gradient-to-tr from-blue-500 to-indigo-600 flex items-center justify-center text-white font-bold shadow-sm">
                  {user?.username?.charAt(0).toUpperCase() || 'U'}
                </div>
                <div className="ml-3">
                  <p className="text-sm font-medium text-gray-700 group-hover:text-gray-900">
                    {user?.username}
                  </p>
                  <p className="text-xs font-medium text-gray-500 capitalize">
                    {user?.role}
                  </p>
                </div>
              </div>
            </div>
          </div>
          <div className="flex-shrink-0 w-14" aria-hidden="true">
            {/* Force sidebar to shrink to fit close icon */}
          </div>
        </div>
      </div>
    </>
  );
};

export default MobileSidebar;
