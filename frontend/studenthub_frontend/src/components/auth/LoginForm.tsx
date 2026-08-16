import { useForm } from "react-hook-form";
import { useNavigate, Link } from "react-router-dom";
import { useState } from "react";
import axios from "axios";
import { login } from "../../api/auth";
import { setTokens } from "../../api/tokenStorage";
import type { LoginRequest } from "../../types/auth";

interface ApiErrorResponse {
    success: boolean;
    message: string;
}

export default function LoginForm() {
    const navigate = useNavigate();
    const [serverError, setServerError] = useState<string | null>(null);
    const [isSubmitting, setIsSubmitting] = useState(false);

    const {
        register,
        handleSubmit,
        formState: { errors },
    } = useForm<LoginRequest>();

    async function onSubmit(data: LoginRequest) {
        setServerError(null);
        setIsSubmitting(true);

        try {
            const response = await login(data);

            setTokens(
                response.data.tokens.access,
                response.data.tokens.refresh,
            );

            // NOTE: assumes a "/dashboard" route exists.
            navigate("/dashboard");
        } catch (err: unknown) {
            let message = "Login failed. Please check your credentials.";

            if (axios.isAxiosError<ApiErrorResponse>(err)) {
                message = err.response?.data?.message ?? message;
            }

            setServerError(message);
        } finally {
            setIsSubmitting(false);
        }
    }

    return (
        <form
            onSubmit={handleSubmit(onSubmit)}
            className="w-full max-w-sm space-y-4 rounded-lg bg-white p-8 shadow-sm"
        >
            <h1 className="mb-2 text-2xl font-semibold text-gray-900">
                Sign in to StudentHub
            </h1>

            <div>
                <input
                    type="email"
                    placeholder="Email"
                    className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                    {...register("email", {
                        required: "Email is required",
                        pattern: {
                            value: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
                            message: "Enter a valid email address",
                        },
                    })}
                />
                {errors.email && (
                    <p className="mt-1 text-sm text-red-600">
                        {errors.email.message}
                    </p>
                )}
            </div>

            <div>
                <input
                    type="password"
                    placeholder="Password"
                    className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                    {...register("password", {
                        required: "Password is required",
                    })}
                />
                {errors.password && (
                    <p className="mt-1 text-sm text-red-600">
                        {errors.password.message}
                    </p>
                )}
            </div>

            {serverError && (
                <p className="text-sm text-red-600" role="alert">
                    {serverError}
                </p>
            )}

            <button
                type="submit"
                disabled={isSubmitting}
                className="w-full rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-60"
            >
                {isSubmitting ? "Signing in..." : "Login"}
            </button>

            <p className="text-center text-sm text-gray-600">
                Don't have an account?{" "}
                <Link to="/register" className="text-blue-600 hover:underline">
                    Register
                </Link>
            </p>
        </form>
    );
}
