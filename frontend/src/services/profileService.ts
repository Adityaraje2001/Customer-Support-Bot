import type { ProfileStats } from '../types/profile';

export const profileService = {
  getStats: async (): Promise<ProfileStats> => {
    // Mocking the backend response since /api/auth/stats or similar doesn't exist yet
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({
          totalConversations: 124,
          openTickets: 3,
          resolvedTickets: 42,
          averageResponseTime: '2.4 hrs'
        });
      }, 500);
    });
  }
};
