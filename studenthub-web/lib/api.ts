const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL as string;

const ACCESS_TOKEN_KEY = "studenthub_access_token";
const REFRESH_TOKEN_KEY = "studenthub_refresh_token";

export function getAccessToken(): string | null {
  if (typeof window === "undefined") return null;
  return window.localStorage.getItem(ACCESS_TOKEN_KEY);
}

export function getRefreshToken(): string | null {
  if (typeof window === "undefined") return null;
  return window.localStorage.getItem(REFRESH_TOKEN_KEY);
}

export function setTokens(access: string, refresh: string) {
  window.localStorage.setItem(ACCESS_TOKEN_KEY, access);
  window.localStorage.setItem(REFRESH_TOKEN_KEY, refresh);
}

export function clearTokens() {
  window.localStorage.removeItem(ACCESS_TOKEN_KEY);
  window.localStorage.removeItem(REFRESH_TOKEN_KEY);
}

export class ApiError extends Error {
  status: number;
  // Backend errors are typically field -> [messages]; kept loose here
  // since different endpoints shape validation errors slightly
  // differently (see DRF ValidationError bodies across the apps).
  details: unknown;

  constructor(message: string, status: number, details: unknown) {
    super(message);
    this.status = status;
    this.details = details;
  }
}

async function refreshAccessToken(): Promise<string | null> {
  const refresh = getRefreshToken();
  if (!refresh) return null;

  const response = await fetch(`${API_BASE_URL}/auth/token/refresh/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ refresh }),
  });

  if (!response.ok) {
    clearTokens();
    return null;
  }

  const body = await response.json();
  const newAccess = body?.data?.access ?? body?.access;

  if (!newAccess) {
    clearTokens();
    return null;
  }

  window.localStorage.setItem(ACCESS_TOKEN_KEY, newAccess);
  return newAccess;
}

interface RequestOptions extends Omit<RequestInit, "body"> {
  body?: unknown;
  auth?: boolean; // defaults to true
}

/**
 * Thin wrapper around fetch for the StudentHub API.
 *
 * - Sends JSON automatically (pass a plain object as `body`).
 * - Attaches the access token unless `auth: false` is passed
 *   (login/register don't need it).
 * - On a 401, tries exactly one silent refresh-and-retry before
 *   giving up -- avoids looping if the refresh token is also dead.
 */
export async function apiFetch<T = unknown>(
  path: string,
  options: RequestOptions = {}
): Promise<T> {
  const { body, auth = true, headers, ...rest } = options;

  const doFetch = async (): Promise<Response> => {
    const finalHeaders: Record<string, string> = {
      "Content-Type": "application/json",
      ...(headers as Record<string, string>),
    };

    if (auth) {
      const token = getAccessToken();
      if (token) finalHeaders["Authorization"] = `Bearer ${token}`;
    }

    return fetch(`${API_BASE_URL}${path}`, {
      ...rest,
      headers: finalHeaders,
      body: body !== undefined ? JSON.stringify(body) : undefined,
    });
  };

  let response = await doFetch();

  if (response.status === 401 && auth) {
    const refreshed = await refreshAccessToken();
    if (refreshed) {
      response = await doFetch();
    }
  }

  const isJson = response.headers
    .get("content-type")
    ?.includes("application/json");
  const payload = isJson ? await response.json() : null;

  if (!response.ok) {
    const message =
      payload?.message || payload?.detail || "Something went wrong.";
    throw new ApiError(message, response.status, payload);
  }

  // Every view in this codebase wraps its payload in
  // success_response({ message, data }) -- unwrap that consistently
  // so callers just get the data they asked for.
  return (payload?.data ?? payload) as T;
}
