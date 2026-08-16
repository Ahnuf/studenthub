"use client";

import {
  createContext,
  useContext,
  useEffect,
  useState,
  ReactNode,
} from "react";
import { useRouter } from "next/navigation";
import { apiFetch, setTokens, clearTokens, getAccessToken, ApiError } from "./api";

export interface User {
  id: number;
  email: string;
  username: string;
  first_name: string;
  last_name: string;
  role: "STUDENT" | "TEACHER" | "ADMIN";
  is_verified: boolean;
  created_at: string;
}

interface AuthContextValue {
  user: User | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (data: {
    email: string;
    username: string;
    first_name: string;
    last_name: string;
    password: string;
    password_confirm: string;
  }) => Promise<void>;
  logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    async function loadUser() {
      if (!getAccessToken()) {
        setLoading(false);
        return;
      }

      try {
        const me = await apiFetch<User>("/auth/me/");
        setUser(me);
      } catch {
        clearTokens();
      } finally {
        setLoading(false);
      }
    }

    loadUser();
  }, []);

  async function login(email: string, password: string) {
    const data = await apiFetch<{ user: User; tokens: { access: string; refresh: string } }>(
      "/auth/login/",
      { method: "POST", auth: false, body: { email, password } }
    );

    setTokens(data.tokens.access, data.tokens.refresh);
    setUser(data.user);
    router.push("/dashboard");
  }

  async function register(payload: {
    email: string;
    username: string;
    first_name: string;
    last_name: string;
    password: string;
    password_confirm: string;
  }) {
    await apiFetch("/auth/register/", {
      method: "POST",
      auth: false,
      body: payload,
    });

    // Registration doesn't log the user in automatically on the
    // backend (it returns id/email only, no tokens) -- send them
    // to login rather than assuming a session exists.
    router.push("/login?registered=1");
  }

  async function logout() {
    const refresh =
      typeof window !== "undefined"
        ? window.localStorage.getItem("studenthub_refresh_token")
        : null;

    try {
      if (refresh) {
        await apiFetch("/auth/logout/", {
          method: "POST",
          body: { refresh },
        });
      }
    } catch {
      // Logging out client-side should succeed even if the
      // blacklist call fails (e.g. token already expired) --
      // there's nothing the user can do about that, and blocking
      // logout on it would strand them in a broken state.
    }

    clearTokens();
    setUser(null);
    router.push("/login");
  }

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth(): AuthContextValue {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}

export { ApiError };
