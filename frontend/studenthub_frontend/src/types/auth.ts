// Shared API envelope -- every StudentHub backend response uses
// this shape: { success, message, data }. Reuse ApiResponse<T>
// for notes.ts/qa.ts/quizzes.ts too, rather than redefining it.
export interface ApiResponse<T> {
    success: boolean;
    message: string;
    data: T;
}

export interface LoginRequest {
    email: string;
    password: string;
}

export interface AuthTokens {
    access: string;
    refresh: string;
}

export interface User {
    id: number;
    email: string;
    username: string;
    first_name: string;
    last_name: string;
    role: "STUDENT" | "TEACHER" | "ADMIN";
    is_verified: boolean;
}

export interface LoginData {
    user: User;
    tokens: AuthTokens;
}

export type LoginResponse = ApiResponse<LoginData>;

export interface RegisterRequest {
    username: string;
    email: string;
    password: string;
    // NOTE: the backend service does
    // validated_data.pop("password_confirm"), which strongly
    // implies RegisterSerializer requires this field. Included
    // here as a best guess -- confirm against the actual
    // RegisterSerializer before wiring up Register.tsx.
    password_confirm: string;
    first_name?: string;
    last_name?: string;
}

export interface RegisterData {
    id: number;
    email: string;
}

export type RegisterResponse = ApiResponse<RegisterData>;