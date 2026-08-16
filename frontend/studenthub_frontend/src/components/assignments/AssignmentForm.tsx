import { useForm } from "react-hook-form";
import { useState } from "react";
import axios from "axios";
import { createAssignment } from "../../api/assignments";
import type { Assignment, AssignmentCreateRequest } from "../../types/assignment";

interface ApiErrorResponse {
    success: boolean;
    message: string;
}

interface Props {
    onCreated: (assignment: Assignment) => void;
}

export default function AssignmentForm({ onCreated }: Props) {
    const [serverError, setServerError] = useState<string | null>(null);
    const [isSubmitting, setIsSubmitting] = useState(false);

    const {
        register,
        handleSubmit,
        reset,
        formState: { errors },
    } = useForm<AssignmentCreateRequest>();

    async function onSubmit(data: AssignmentCreateRequest) {
        setServerError(null);
        setIsSubmitting(true);

        try {
            const response = await createAssignment(data);
            onCreated(response.data);
            reset();
        } catch (err: unknown) {
            let message = "Failed to create assignment.";

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
            className="space-y-3 rounded-lg bg-white p-6 shadow-sm"
        >
            <h2 className="font-semibold text-gray-900">Add Assignment</h2>

            <div className="grid gap-3 md:grid-cols-2">
                <div>
                    <input
                        type="text"
                        placeholder="Course name"
                        className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                        {...register("course_name", {
                            required: "Course name is required",
                        })}
                    />
                    {errors.course_name && (
                        <p className="mt-1 text-sm text-red-600">
                            {errors.course_name.message}
                        </p>
                    )}
                </div>

                <div>
                    <input
                        type="text"
                        placeholder="Assignment title"
                        className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                        {...register("title", {
                            required: "Title is required",
                        })}
                    />
                    {errors.title && (
                        <p className="mt-1 text-sm text-red-600">
                            {errors.title.message}
                        </p>
                    )}
                </div>
            </div>

            <div>
                <textarea
                    placeholder="Description (optional)"
                    rows={2}
                    className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                    {...register("description")}
                />
            </div>

            <div className="flex items-end gap-3">
                <div>
                    <label className="mb-1 block text-sm font-medium text-gray-700">
                        Due date
                    </label>
                    <input
                        type="date"
                        className="rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                        {...register("due_date", {
                            required: "Due date is required",
                        })}
                    />
                    {errors.due_date && (
                        <p className="mt-1 text-sm text-red-600">
                            {errors.due_date.message}
                        </p>
                    )}
                </div>

                <button
                    type="submit"
                    disabled={isSubmitting}
                    className="rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-60"
                >
                    {isSubmitting ? "Adding..." : "Add"}
                </button>
            </div>

            {serverError && (
                <p className="text-sm text-red-600" role="alert">
                    {serverError}
                </p>
            )}
        </form>
    );
}
