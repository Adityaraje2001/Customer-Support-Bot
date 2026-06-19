import React, { createContext, useState, useEffect } from 'react';
import type { ReactNode } from 'react';
import type { User, LoginRequest, RegisterRequest } from '../types/auth';
import { authService } from '../services/authService';
import { getToken } from '../utils/token';

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  loading: boolean;
  login: (credentials: LoginRequest) => Promise<User>;
  register: (data: RegisterRequest) => Promise<User>;
  logout: () => void;
}

export const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const initAuth = async () => {
      const token = getToken();
      if (token) {
        try {
          const currentUser = await authService.getCurrentUser();
          setUser(currentUser);
        } catch (error) {
          console.error('Failed to restore session', error);
          authService.logout();
        }
      }
      setLoading(false);
    };

    initAuth();
  }, []);

  const login = async (credentials: LoginRequest): Promise<User> => {
    const currentUser = await authService.login(credentials);
    setUser(currentUser);
    return currentUser;
  };

  const register = async (data: RegisterRequest): Promise<User> => {
    await authService.register(data);
    return await login({ email: data.email, password: data.password });
  };

  const logout = () => {
    authService.logout();
    setUser(null);
  };

  const value = {
    user,
    isAuthenticated: !!user,
    loading,
    login,
    register,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
