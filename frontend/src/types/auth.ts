export interface User {
  id: number;
  username: string;
  email: string;
  role: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
  role: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
}
