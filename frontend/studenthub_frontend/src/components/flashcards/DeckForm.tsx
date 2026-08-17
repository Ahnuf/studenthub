"use no memo";

import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import axios from "axios";

import { createDeck, updateDeck } from "../../api/flashcards";
import { getCourses } from "../../api/academic";

import type {
    FlashcardDeck,
    FlashcardDeckCreateRequest,
    FlashcardDeckUpdateRequest,
} from "../../types/flashcards";

import type { CourseOption } from "../../api/academic";

interface Props {
    editingDeck?: FlashcardDeck | null;
    onCreated: (deck: FlashcardDeck) => void;
    onUpdated: (deck: FlashcardDeck) => void;
    onCancelEdit: () => void;
}

interface DeckFormData {
    course: number;
    title: string;
    description: string;
}

interface ApiErrorResponse {
    success: boolean;
    message: string;
}

export default function DeckForm({
    editingDeck,
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
    } = useForm<DeckFormData>({
        defaultValues: {
            course: editingDeck?.course ?? 0,
            title: editingDeck?.title ?? "",
            description: editingDeck?.description ?? "",
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
            course: editingDeck?.course ?? 0,
            title: editingDeck?.title ?? "",
            description: editingDeck?.description ?? "",
        });
    }, [editingDeck, reset]);

    async function onSubmit(data: DeckFormData) {
        setServerError(null);
        setIsSubmitting(true);

        try {
            if (editingDeck) {
                const payload: FlashcardDeckUpdateRequest = {
                    title: data.title,
                    description: data.description,
                };

                const updatedDeck = await updateDeck(
                    editingDeck.id,
                    payload,
                );

                onUpdated(updatedDeck);
            } else {
                const payload: FlashcardDeckCreateRequest = {
                    course: data.course,
                    title: data.title,
                    description: data.description,
                };

                const createdDeck = await createDeck(payload);

                onCreated(createdDeck);

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
                        "Failed to save deck.",
                );
            } else {
                setServerError("Failed to save deck.");
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
                {editingDeck
                    ? "Edit Deck"
                    : "Create Flashcard Deck"}
            </h2>

            {!editingDeck && (
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

                    <p className="mt-1 text-xs text-gray-500">
                        A deck stays attached to this course after creation.
                    </p>
                </div>
            )}

            {editingDeck && (
                <div className="rounded-md bg-gray-50 px-3 py-2">
                    <p className="text-xs text-gray-500">
                        Course
                    </p>
                    <p className="text-sm font-medium text-gray-800">
                        {editingDeck.course_title}
                    </p>
                </div>
            )}

            <div>
                <label className="mb-1 block text-sm font-medium text-gray-700">
                    Title
                </label>

                <input
                    type="text"
                    placeholder="e.g. Database Systems Revision"
                    {...register("title", {
                        required: "Deck title is required",
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
                        : editingDeck
                          ? "Save Changes"
                          : "Create Deck"}
                </button>

                {editingDeck && (
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