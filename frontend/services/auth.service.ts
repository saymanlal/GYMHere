import { apiService, ApiResponse } from "./api";

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  password: string;
  firstName: string;
  lastName: string;
  phone: string;
}

export interface AuthTokens {
  access: string;
  refresh: string;
}

export interface User {
  id: string;
  email: string;
  firstName: string;
  lastName: string;
  phone: string;
  role: {
    id: string;
    name: string;
    permissions: Record<string, string[]>;
  };
  isActive: boolean;
  lastLogin: string;
  createdAt: string;
}

export interface AuthResponse {
  user: User;
  tokens: AuthTokens;
}

class AuthService {
  async login(credentials: LoginCredentials): Promise<AuthResponse> {
    const response = await apiService.post<ApiResponse<AuthResponse>>(
      "/auth/login/",
      credentials
    );
    
    if (response.success && response.data) {
      const { tokens } = response.data;
      apiService.setAuthTokens(tokens.access, tokens.refresh);
    }
    
    return response.data;
  }

  async register(data: RegisterData): Promise<AuthResponse> {
    const response = await apiService.post<ApiResponse<AuthResponse>>(
      "/auth/register/",
      data
    );
    
    if (response.success && response.data) {
      const { tokens } = response.data;
      apiService.setAuthTokens(tokens.access, tokens.refresh);
    }
    
    return response.data;
  }

  async logout(): Promise<void> {
    try {
      await apiService.post("/auth/logout/");
    } finally {
      apiService.clearAuthTokens();
    }
  }

  async getCurrentUser(): Promise<User> {
    const response = await apiService.get<ApiResponse<User>>("/auth/me/");
    return response.data;
  }

  async updateProfile(data: Partial<User>): Promise<User> {
    const response = await apiService.patch<ApiResponse<User>>("/auth/me/", data);
    return response.data;
  }

  async changePassword(oldPassword: string, newPassword: string): Promise<void> {
    await apiService.post("/auth/change-password/", {
      oldPassword,
      newPassword,
    });
  }

  async resetPassword(email: string): Promise<void> {
    await apiService.post("/auth/reset-password/", { email });
  }

  async confirmResetPassword(token: string, newPassword: string): Promise<void> {
    await apiService.post("/auth/reset-password/confirm/", {
      token,
      newPassword,
    });
  }

  isAuthenticated(): boolean {
    return apiService.isAuthenticated();
  }
}

export const authService = new AuthService();