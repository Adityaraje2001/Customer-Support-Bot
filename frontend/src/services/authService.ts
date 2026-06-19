import authApi from '../api/authApi';
import type { LoginRequest, LoginResponse, RegisterRequest, User } from '../types/auth';
import { setToken, removeToken } from '../utils/token';

export const authService = {
  login: async (credentials: LoginRequest): Promise<User> => {
    const formData = new URLSearchParams();
    formData.append('username', credentials.email); // OAuth2 expects username
    formData.append('password', credentials.password);

    const response = await authApi.post<LoginResponse>('/auth/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });

    setToken(response.data.access_token);
    return await authService.getCurrentUser();
  },

  register: async (data: RegisterRequest): Promise<void> => {
    await authApi.post('/auth/register', data);
  },

  getCurrentUser: async (): Promise<User> => {
    const response = await authApi.get<User>('/auth/me');
    return response.data;
  },

  logout: () => {
    removeToken();
  },
};
