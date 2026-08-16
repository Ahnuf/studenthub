import { useForm } from "react-hook-form";
import { useNavigate, Link } from "react-router-dom";
import { useState } from "react";
import axios from "axios";
import { register as registerUser } from "../../api/auth";
import type { RegisterRequest } from "../../types/auth";

interface ApiErrorResponse {
    success: boolean;
    message: string;
}

export default function RegisterForm() {
    const navigate = useNavigate();
    const [serverError, setServerError] = useState<string | null>(null);
    const [isSubmitting, setIsSubmitting] = useState(false);

    const {
        register,
        handleSubmit,
        getValues,
        formState: { errors },
    } = useForm<RegisterRequest>();

    async function onSubmit(data: RegisterRequest) {
        setServerError(null);
        setIsSubmitting(true);

        try {
            await registerUser(data);

            // RegisterView returns {id, email} only -- no tokens.
            // Registration doesn't auto-login, so send them to
            // login instead of the dashboard.
            navigate("/login", {
                state: { registered: true },
            });
        } catch (err: unknown) {
            let message = "Registration failed. Please try again.";

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
                Create your StudentHub account
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
                    type="text"
                    placeholder="Username"
                    className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                    {...register("username", {
                        required: "Username is required",
                    })}
                />
                {errors.username && (
                    <p className="mt-1 text-sm text-red-600">
                        {errors.username.message}
                    </p>
                )}
            </div>

            <div className="flex gap-3">
                <div className="flex-1">
                    <input
                        type="text"
                        placeholder="First name (optional)"
                        className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                        {...register("first_name")}
                    />
                </div>
                <div className="flex-1">
                    <input
                        type="text"
                        placeholder="Last name (optional)"
                        className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                        {...register("last_name")}
                    />
                </div>
            </div>

            <div>
                <input
                    type="password"
                    placeholder="Password"
                    className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                    {...register("password", {
                        required: "Password is required",
                        minLength: {
                            value: 8,
                            message: "Password must be at least 8 characters",
                        },
                    })}
                />
                {errors.password && (
                    <p className="mt-1 text-sm text-red-600">
                        {errors.password.message}
                    </p>
                )}
            </div>

            <div>
                <input
                    type="password"
                    placeholder="Confirm password"
                    className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                    {...register("password_confirm", {
                        required: "Please confirm your password",
                        validate: (value) =>
                            value === getValues("password") ||
                            "Passwords do not match",
                    })}
                />
                {errors.password_confirm && (
                    <p className="mt-1 text-sm text-red-600">
                        {errors.password_confirm.message}
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
                {isSubmitting ? "Creating account..." : "Register"}
            </button>

            <p className="text-center text-sm text-gray-600">
                Already have an account?{" "}
                <Link to="/login" className="text-blue-600 hover:underline">
                    Sign in
                </Link>
            </p>
        </form>
    );
}
