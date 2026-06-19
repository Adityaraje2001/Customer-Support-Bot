import React from 'react';
import type { User } from '../../types/auth';

interface ProfileCardProps {
  user: User | null;
}

const ProfileCard: React.FC<ProfileCardProps> = ({ user }) => {
  if (!user) return null;

  const getInitials = (name: string) => name ? name.charAt(0).toUpperCase() : 'U';

  return (
    <div className="bg-white rounded-2xl shadow-sm border border-gray-200 overflow-hidden">
      <div className="h-32 bg-gradient-to-r from-blue-600 to-indigo-600"></div>
      <div className="px-6 pb-6">
        <div className="relative flex justify-center -mt-12 mb-4">
          <div className="h-24 w-24 bg-white rounded-full p-1 shadow-lg">
            <div className="h-full w-full rounded-full bg-gradient-to-tr from-blue-500 to-indigo-600 flex items-center justify-center text-3xl text-white font-bold">
              {getInitials(user.username)}
            </div>
          </div>
        </div>
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900">{user.username}</h2>
          <p className="text-gray-500 mb-4">{user.email}</p>
          <div className="inline-flex items-center px-3 py-1 rounded-full bg-blue-50 text-blue-700 text-sm font-medium capitalize mb-4">
            {user.role}
          </div>
        </div>
        <div className="border-t border-gray-100 pt-4 mt-2">
          <div className="flex justify-between items-center text-sm">
            <span className="text-gray-500">Account Created</span>
            <span className="font-medium text-gray-900">
              {/* Mock date as it's not in the User type yet */}
              {new Date().toLocaleDateString(undefined, { year: 'numeric', month: 'long', day: 'numeric' })}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProfileCard;
