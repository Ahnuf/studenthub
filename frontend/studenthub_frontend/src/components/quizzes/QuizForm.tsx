"use no memo";

import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import axios from "axios";

import { createQuiz, updateQuiz } from "../../api/quizzes";
import { getCourses } from "../../api/academic";

import type {
    Quiz,
    QuizCreateRequest,
    QuizUpdateRequest,
} from "../../types/quizzes";

import type { CourseOption } from "../../api/academic";

interface Props {
    editingQuiz?: Quiz | null;
    onCreated: (quiz: Quiz) => void;
    onUpdated: (quiz: Quiz) => void;
    onCancelEdit: () => void;
}

interface QuizFormData {
    course: number;
    title: string;
    description: string;
}

interface ApiErrorResponse {
    success: boolean;
    message: string;
}

export default function QuizForm({
    editingQuiz,
    onCreated,
    onUpdated,
    onCancelEdit,
}: Props) {
    const [courses, setCourses] = useState<CourseOption[]>([]);
    const [isLoadingCourses, setIsLoadingCourses] = useState(true);
    const [serverError, setServerError] = useState<string | null>(
        null,
    );
    const [isSubmitting, setIsSubmitting] = useState(false);

    const {
        register,
        handleSubmit,
        reset,
        formState: { errors },
    } = useForm<QuizFormData>({
        defaultValues: {
            course: editingQuiz?.course ?? 0,
            title: editingQuiz?.title ?? "",
            description: editingQuiz?.description ?? "",
        },
    });

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

    useEffect(() => {
        reset({
            course: editingQuiz?.course ?? 0,
            title: editingQuiz?.title ?? "",
            description: editingQuiz?.description ?? "",
        });
    }, [editingQuiz, reset]);

    async function onSubmit(data: QuizFormData) {
        setServerError(null);
        setIsSubmitting(true);

        try {
            if (editingQuiz) {
                const payload: QuizUpdateRequest = {
                    title: data.title,
                    description: data.description,
                };

                const updatedQuiz = await updateQuiz(
                    editingQuiz.id,
                    payload,
                );

                onUpdated(updatedQuiz);
            } else {
                const payload: QuizCreateRequest = {
                    course: data.course,
                    title: data.title,
                    description: data.description,
                };

                const createdQuiz = await createQuiz(payload);

                onCreated(createdQuiz);

                reset({
                    course: 0,
                    title: "",
                    description: "",
                });
            }
        } catch (err: unknown) {
            if (axios.isAxiosError<ApiErrorResponse>(err)) {
                setServerError(
                    err.response?.data?.message ??
                        "Failed to save quiz.",
                );
            } else {
                setServerError("Failed to save quiz.");
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
                {editingQuiz ? "Edit Quiz" : "Create Quiz"}
            </h2>

            {!editingQuiz && (
                <div>
                    <label className="mb-1 block text-sm font-medium text-gray-700">
                        Course
                    </label>

                    <select
                        disabled={isLoadingCourses}
                        {...register("course", {
                            required: "Course is required",
                            valueAsNumber: true,
                            validate: (value) =>
                                value > 0 ||
                                "Please select a course",
                        })}
                        className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 disabled:bg-gray-100"
                    >
                        <option value={0}>
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
            )}

            {editingQuiz && (
                <div className="rounded-md bg-gray-50 px-3 py-2">
                    <p className="text-xs text-gray-500">
                        Course
                    </p>
                    <p className="text-sm font-medium text-gray-800">
                        {editingQuiz.course_title}
                    </p>
                </div>
            )}

            <div>
                <label className="mb-1 block text-sm font-medium text-gray-700">
                    Title
                </label>

                <input
                    type="text"
                    placeholder="e.g. Database Systems Quiz"
                    {...register("title", {
                        required: "Quiz title is required",
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
                    Description
                </label>

                <textarea
                    rows={4}
                    placeholder="Description (optional)"
                    {...register("description")}
                    className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                />
            </div>

            {serverError && (
                <p
                    className="text-sm text-red-600"
                    role="alert"
                >
                    {serverError}
                </p>
            )}

            <div className="flex gap-3">
                <button
                    type="submit"
                    disabled={isSubmitting || isLoadingCourses}
                    className="rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-60"
                >
                    {isSubmitting
                        ? "Saving..."
                        : editingQuiz
                          ? "Save Changes"
                          : "Create Quiz"}
                </button>

                {editingQuiz && (
                    <button
                        type="button"
                        onClick={onCancelEdit}
                        disabled={isSubmitting}
                        className="rounded-md border border-gray-300 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-60"
                    >
                        Cancel
                    </button>
                )}
            </div>
        </form>
    );
}