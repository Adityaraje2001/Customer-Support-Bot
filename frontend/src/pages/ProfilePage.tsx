import React, { useEffect, useState } from 'react';
import { useAuth } from '../hooks/useAuth';
import { profileService } from '../services/profileService';
import type { ProfileStats as ProfileStatsType } from '../types/profile';
import ProfileCard from '../components/profile/ProfileCard';
import ProfileStats from '../components/profile/ProfileStats';
import AccountSettings from '../components/profile/AccountSettings';
import ChangePasswordForm from '../components/profile/ChangePasswordForm';

const ProfilePage: React.FC = () => {
  const { user } = useAuth();
  const [stats, setStats] = useState<ProfileStatsType | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadStats = async () => {
      try {
        setLoading(true);
        const data = await profileService.getStats();
        setStats(data);
      } catch (error) {
        console.error('Failed to load profile stats:', error);
      } finally {
        setLoading(false);
      }
    };

    loadStats();
  }, []);

  return (
    <div className="max-w-6xl mx-auto space-y-6 pb-10">
      <div className="flex flex-col md:flex-row gap-6">
        {/* Left Column: Profile Card */}
        <div className="w-full md:w-1/3">
          <ProfileCard user={user} />
        </div>

        {/* Right Column: Stats */}
        <div className="w-full md:w-2/3">
          <ProfileStats stats={stats} loading={loading} />
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Settings */}
        <AccountSettings />

        {/* Change Password */}
        <ChangePasswordForm />
      </div>
    </div>
  );
};

export default ProfilePage;
