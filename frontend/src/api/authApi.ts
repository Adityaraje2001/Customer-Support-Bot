import axios from 'axios';
import { getToken } from '../utils/token';

const authApi = axios.create({
  baseURL: 'http://localhost:8000/api',
});

authApi.interceptors.request.use(
  (config) => {
    const token = getToken();
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default authApi;
