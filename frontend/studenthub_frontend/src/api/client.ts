import axios, { type AxiosError, type InternalAxiosRequestConfig } from "axios";
import { getAccessToken, getRefreshToken, setTokens, clearTokens } from "./tokenStorage";

const BASE_URL = "http://127.0.0.1:8000/api/v1";

const api = axios.create({
    baseURL: BASE_URL,
    headers: {
        "Content-Type": "application/json",
    },
    timeout: 10000,
});

// Attach the access token to every outgoing request, if one exists.
api.interceptors.request.use((config) => {
    const token = getAccessToken();

    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
});

// --- 401 handling: attempt one silent refresh, then retry ---
//
// If several requests fail with 401 at the same moment (e.g. a
// page fires multiple API calls at once), only ONE refresh call
// should actually happen -- the rest queue up and get the same
// new token once it's ready, rather than each firing their own
// refresh request.

let isRefreshing = false;
let pendingRequests: Array<(token: string) => void> = [];

function onRefreshed(newAccessToken: string) {
    pendingRequests.forEach((callback) => callback(newAccessToken));
    pendingRequests = [];
}

interface RetryableConfig extends InternalAxiosRequestConfig {
    _retry?: boolean;
}

api.interceptors.response.use(
    (response) => response,
    async (error: AxiosError) => {
        const originalRequest = error.config as RetryableConfig;

        const isLoginRequest = originalRequest?.url?.includes("/auth/login/");

        if (
            error.response?.status !== 401 ||
            originalRequest._retry ||
            isLoginRequest
        ) {
            // Not a token-expiry case (or already retried once, or
            // it's a login attempt itself -- a wrong password
            // shouldn't trigger a refresh attempt) -- just fail
            // normally.
            return Promise.reject(error);
        }

        const refreshToken = getRefreshToken();

        if (!refreshToken) {
            clearTokens();
            window.location.href = "/login";
            return Promise.reject(error);
        }

        if (isRefreshing) {
            // A refresh is already in flight -- wait for it, then
            // retry this request with whatever token it produces.
            return new Promise((resolve) => {
                pendingRequests.push((newToken: string) => {
                    originalRequest.headers.Authorization = `Bearer ${newToken}`;
                    resolve(api(originalRequest));
                });
            });
        }

        originalRequest._retry = true;
        isRefreshing = true;

        try {
            // Bare axios call, NOT the `api` instance -- avoids
            // this same interceptor recursively handling a failed
            // refresh call.
            const response = await axios.post(
                `${BASE_URL}/auth/token/refresh/`,
                { refresh: refreshToken },
            );

            const { access, refresh } = response.data.data;
            setTokens(access, refresh);

            onRefreshed(access);

            originalRequest.headers.Authorization = `Bearer ${access}`;
            return api(originalRequest);
        } catch (refreshError) {
            clearTokens();
            window.location.href = "/login";
            return Promise.reject(refreshError);
        } finally {
            isRefreshing = false;
        }
    },
);

export default api;