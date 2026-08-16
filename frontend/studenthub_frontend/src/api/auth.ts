import api from "./client";

import type {
    LoginRequest,
    LoginResponse,
    RegisterRequest,
    RegisterResponse,
} from "../types/auth";

export async function login(data: LoginRequest): Promise<LoginResponse> {
    const response = await api.post<LoginResponse>("/auth/login/", data);

    return response.data;
}

export async function register(data: RegisterRequest): Promise<RegisterResponse> {
    const response = await api.post<RegisterResponse>("/auth/register/", data);

    return response.data;
}

export async function logout(refreshToken: string): Promise<void> {
    // ASSUMPTION: LogoutSerializer expects { refresh }, matching
    // TokenRefreshSerializer's field naming convention -- not
    // confirmed against the actual serializer. If it errors, the
    // caller (AppShell) still clears local tokens regardless.
    await api.post("/auth/logout/", { refresh: refreshToken });
}