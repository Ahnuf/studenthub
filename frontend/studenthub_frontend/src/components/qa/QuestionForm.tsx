"use no memo";

import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import axios from "axios";

import { createQuestion } from "../../api/qa";
import { getCourses, type CourseOption } from "../../api/academic";

import type {
    QuestionCreateRequest,
    QuestionDetail,
} from "../../types/qa";

interface Props {
    onCreated: (question: QuestionDetail) => void;
}

interface QuestionFormData {
    course: number;
    title: string;
    body: string;
}

interface ApiErrorResponse {
    success: boolean;
    message: string;
}

export default function QuestionForm({ onCreated }: Props) {
    const [courses, setCourses] = useState<CourseOption[]>([]);
    const [isLoadingCourses, setIsLoadingCourses] = useState(true);
    const [serverError, setServerError] = useState<string | null>(null);
    const [isSubmitting, setIsSubmitting] = useState(false);

    const {
        register,
        handleSubmit,
        reset,
        formState: { errors },
    } = useForm<QuestionFormData>();

    useEffect(() => {
        async function loadCourses() {
            try {
                const data = await getCourses();
                setCourses(data);
            } catch (err: unknown) {
                if (axios.isAxiosError<ApiErrorResponse>(err)) {
                    setServerError(
                        err.response?.data?.message ??
                            "Failed to load courses.",
                    );
                } else {
                    setServerError("Failed to load courses.");
                }
            } finally {
                setIsLoadingCourses(false);
            }
        }

        loadCourses();
    }, []);

    async function onSubmit(data: QuestionFormData) {
        setServerError(null);
        setIsSubmitting(true);

        try {
            const payload: QuestionCreateRequest = {
                course: data.course,
                title: data.title,
                body: data.body,
            };

            const question = await createQuestion(payload);

            onCreated(question);
            reset();
        } catch (err: unknown) {
            if (axios.isAxiosError<ApiErrorResponse>(err)) {
                setServerError(
                    err.response?.data?.message ??
                        "Failed to post question.",
                );
            } else {
                setServerError("Failed to post question.");
            }
        } finally {
            setIsSubmitting(false);
        }
    }

    return (
        <form
            onSubmit={handleSubmit(onSubmit)}
            className="space-y-4 rounded-lg bg-white p-6 shadow-sm"
        >
            <h2 className="font-semibold text-gray-900">
                Ask a Question
            </h2>

            <div>
                <label className="mb-1 block text-sm font-medium text-gray-700">
                    Course
                </label>

                <select
                    disabled={isLoadingCourses}
                    {...register("course", {
                        required: "Course is required",
                        valueAsNumber: true,
                    })}
                    className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 disabled:bg-gray-100"
                >
                    <option value="">
                        {isLoadingCourses
                            ? "Loading courses..."
                            : "Select a course"}
                    </option>

                    {courses.map((course) => (
                        <option
                            key={course.course}
                            value={course.course}
                        >
                            {course.course_code} — {course.title}
                        </option>
                    ))}
                </select>

                {errors.course && (
                    <p className="mt-1 text-sm text-red-600">
                        {errors.course.message}
                    </p>
                )}
            </div>

            <div>
                <label className="mb-1 block text-sm font-medium text-gray-700">
                    Title
                </label>

                <input
                    type="text"
                    placeholder="What do you need help with?"
                    {...register("title", {
                        required: "Title is required",
                    })}
                    className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                />

                {errors.title && (
                    <p className="mt-1 text-sm text-red-600">
                        {errors.title.message}
                    </p>
                )}
            </div>

            <div>
                <label className="mb-1 block text-sm font-medium text-gray-700">
                    Question
                </label>

                <textarea
                    rows={6}
                    placeholder="Describe your question..."
                    {...register("body", {
                        required: "Question body is required",
                    })}
                    className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                />

                {errors.body && (
                    <p className="mt-1 text-sm text-red-600">
                        {errors.body.message}
                    </p>
                )}
            </div>

            {serverError && (
                <p
                    className="text-sm text-red-600"
                    role="alert"
                >
                    {serverError}
                </p>
            )}

            <button
                type="submit"
                disabled={isSubmitting || isLoadingCourses}
                className="rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-60"
            >
                {isSubmitting
                    ? "Posting..."
                    : "Post Question"}
            </button>
        </form>
    );
}