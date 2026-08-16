"use client";

import { useState } from "react";
import Link from "next/link";
import { useAuth, ApiError } from "@/lib/auth-context";

export default function RegisterPage() {
  const { register } = useAuth();

  const [form, setForm] = useState({
    email: "",
    username: "",
    first_name: "",
    last_name: "",
    password: "",
    password_confirm: "",
  });
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  function update(field: keyof typeof form, value: string) {
    setForm((prev) => ({ ...prev, [field]: value }));
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);

    if (form.password !== form.password_confirm) {
      setError("Passwords do not match.");
      return;
    }

    setSubmitting(true);

    try {
      await register(form);
    } catch (err) {
      setError(
        err instanceof ApiError
          ? err.message
          : "Couldn't reach the server. Try again."
      );
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="auth-shell">
      <div className="auth-card">
        <div className="auth-eyebrow">StudentHub</div>
        <h1>Create your account</h1>

        {error && <div className="form-error">{error}</div>}

        <form onSubmit={handleSubmit}>
          <div className="field">
            <label htmlFor="first_name">First name</label>
            <input
              id="first_name"
              required
              value={form.first_name}
              onChange={(e) => update("first_name", e.target.value)}
            />
          </div>

          <div className="field">
            <label htmlFor="last_name">Last name</label>
            <input
              id="last_name"
              required
              value={form.last_name}
              onChange={(e) => update("last_name", e.target.value)}
            />
          </div>

          <div className="field">
            <label htmlFor="username">Username</label>
            <input
              id="username"
              required
              value={form.username}
              onChange={(e) => update("username", e.target.value)}
            />
          </div>

          <div className="field">
            <label htmlFor="email">Email</label>
            <input
              id="email"
              type="email"
              autoComplete="email"
              required
              value={form.email}
              onChange={(e) => update("email", e.target.value)}
            />
          </div>

          <div className="field">
            <label htmlFor="password">Password</label>
            <input
              id="password"
              type="password"
              autoComplete="new-password"
              required
              minLength={8}
              value={form.password}
              onChange={(e) => update("password", e.target.value)}
            />
          </div>

          <div className="field">
            <label htmlFor="password_confirm">Confirm password</label>
            <input
              id="password_confirm"
              type="password"
              autoComplete="new-password"
              required
              value={form.password_confirm}
              onChange={(e) => update("password_confirm", e.target.value)}
            />
          </div>

          <button className="button-primary" type="submit" disabled={submitting}>
            {submitting ? "Creating account\u2026" : "Create account"}
          </button>
        </form>

        <div className="form-footer">
          Already have an account? <Link href="/login">Sign in</Link>
        </div>
      </div>
    </div>
  );
}
