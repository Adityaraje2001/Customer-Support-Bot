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
  History,
  BookOpen,
  ThumbsUp
} from 'lucide-react';

const Sidebar: React.FC = () => {
  const { user } = useAuth();
  const location = useLocation();

  const navItems = [
    { name: 'Dashboard', path: '/dashboard', icon: LayoutDashboard, roles: ['customer', 'admin'] },
    { name: 'Chat', path: '/chat', icon: MessageSquare, roles: ['customer', 'admin'] },
    { name: 'My Tickets', path: '/my-tickets', icon: Ticket, roles: ['customer', 'admin'] },
    { name: 'Admin Tickets', path: '/admin/tickets', icon: Shield, roles: ['admin'] },
    { name: 'Knowledge Base', path: '/admin/knowledge-base', icon: BookOpen, roles: ['admin'] },
    { name: 'Analytics', path: '/admin/analytics', icon: BarChart, roles: ['admin'] },
    { name: 'Feedback', path: '/admin/feedback', icon: ThumbsUp, roles: ['admin'] },
    { name: 'Conversations', path: '/conversations', icon: History, roles: ['customer', 'admin'] },
    { name: 'Profile', path: '/profile', icon: User, roles: ['customer', 'admin'] },
  ];

  const filteredItems = navItems.filter(item => 
    user && item.roles.includes(user.role)
  );

  return (
    <aside className="hidden lg:flex lg:flex-col lg:w-64 lg:fixed lg:inset-y-0 bg-white border-r border-gray-200">
      <div className="flex-1 flex flex-col min-h-0 pt-5 pb-4 overflow-y-auto">
        <div className="flex items-center flex-shrink-0 px-6">
          <span className="text-2xl font-black bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
            SupportBot
          </span>
        </div>
        <nav className="mt-8 flex-1 px-4 space-y-2">
          {filteredItems.map((item) => {
            const isActive = location.pathname.startsWith(item.path);
            const Icon = item.icon;
            return (
              <NavLink
                key={item.name}
                to={item.path}
                className={`group flex items-center px-3 py-2.5 text-sm font-medium rounded-xl transition-all duration-200 ${
                  isActive
                    ? 'bg-blue-50 text-blue-700 shadow-sm'
                    : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                }`}
              >
                <Icon
                  className={`flex-shrink-0 -ml-1 mr-3 h-5 w-5 transition-colors ${
                    isActive ? 'text-blue-600' : 'text-gray-400 group-hover:text-gray-500'
                  }`}
                  aria-hidden="true"
                />
                <span className="truncate">{item.name}</span>
                {isActive && (
                  <div className="ml-auto w-1.5 h-1.5 rounded-full bg-blue-600"></div>
                )}
              </NavLink>
            );
          })}
        </nav>
      </div>
      <div className="flex-shrink-0 flex border-t border-gray-200 p-4">
        <div className="flex items-center w-full">
          <div className="h-9 w-9 rounded-full bg-gradient-to-tr from-blue-500 to-indigo-600 flex items-center justify-center text-white font-bold shadow-sm">
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
    </aside>
  );
};

export default Sidebar;
