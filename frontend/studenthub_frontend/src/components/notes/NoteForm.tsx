/* eslint-disable react-hooks/refs */
"use no memo";

import { useEffect, useRef, useState } from "react";
import { useForm } from "react-hook-form";
import axios from "axios";

import { createNote } from "../../api/notes";
import { getCourses, type CourseOption } from "../../api/academic";

import type {
    Note,
    NoteCreateRequest,
} from "../../types/notes";

interface ApiErrorResponse {
    success: boolean;
    message: string;
}

interface Props {
    onCreated: (note: Note) => void;
}

const MAX_FILE_SIZE = 20 * 1024 * 1024;

const ALLOWED_EXTENSIONS = [
    "pdf",
    "doc",
    "docx",
    "ppt",
    "pptx",
    "jpg",
    "jpeg",
    "png",
];

interface NoteFormData {
    course: number;
    main_heading: string;
    sub_heading: string;
    description: string;
}

export default function NoteForm({ onCreated }: Props) {
    const [courses, setCourses] = useState<CourseOption[]>([]);
    const [isLoadingCourses, setIsLoadingCourses] = useState(true);
    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const [fileError, setFileError] = useState<string | null>(null);
    const [serverError, setServerError] = useState<string | null>(null);
    const [isSubmitting, setIsSubmitting] = useState(false);

    const fileInputRef = useRef<HTMLInputElement | null>(null);

    const {
        register,
        handleSubmit,
        reset,
        formState: { errors },
    } = useForm<NoteFormData>();

    useEffect(() => {
        async function loadCourses() {
            try {
                const response = await getCourses();
                setCourses(response);
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

    function handleFileChange(
        event: React.ChangeEvent<HTMLInputElement>,
    ) {
        setFileError(null);

        const file = event.target.files?.[0] ?? null;

        if (!file) {
            setSelectedFile(null);
            return;
        }

        if (file.size > MAX_FILE_SIZE) {
            setSelectedFile(null);
            setFileError("File size must not exceed 20 MB.");

            if (fileInputRef.current) {
                fileInputRef.current.value = "";
            }

            return;
        }

        const extension = file.name
            .split(".")
            .pop()
            ?.toLowerCase();

        if (
            !extension ||
            !ALLOWED_EXTENSIONS.includes(extension)
        ) {
            setSelectedFile(null);
            setFileError(
                "Unsupported file type. Allowed types: PDF, DOC, DOCX, PPT, PPTX, JPG, JPEG, PNG.",
            );

            if (fileInputRef.current) {
                fileInputRef.current.value = "";
            }

            return;
        }

        setSelectedFile(file);
    }

    async function onSubmit(data: NoteFormData) {
        setServerError(null);
        setFileError(null);

        if (!selectedFile) {
            setFileError("Please select a file.");
            return;
        }

        setIsSubmitting(true);

        try {
            const payload: NoteCreateRequest = {
                course: data.course,
                main_heading: data.main_heading,
                sub_heading: data.sub_heading,
                description: data.description,
                file: selectedFile,
            };

            const note = await createNote(payload);

            onCreated(note);

            reset();
            setSelectedFile(null);

            if (fileInputRef.current) {
                fileInputRef.current.value = "";
            }
        } catch (err: unknown) {
            let message = "Failed to upload note.";

            if (axios.isAxiosError<ApiErrorResponse>(err)) {
                message =
                    err.response?.data?.message ?? message;
            }

            setServerError(message);
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
                Upload Note
            </h2>

            <div>
                <label className="mb-1 block text-sm font-medium text-gray-700">
                    Course
                </label>

                <select
                    disabled={isLoadingCourses}
                    className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 disabled:bg-gray-100"
                    {...register("course", {
                        required: "Course is required",
                        valueAsNumber: true,
                    })}
                >
                    <option value="">
                        {isLoadingCourses
                            ? "Loading courses..."
                            : "Select a course"}
                    </option>

                    {courses.map((course) => (
                        <option
                            key={course.id}
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
                    Main Heading
                </label>

                <input
                    type="text"
                    placeholder="Note heading"
                    className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                    {...register("main_heading", {
                        required: "Main heading is required",
                    })}
                />

                {errors.main_heading && (
                    <p className="mt-1 text-sm text-red-600">
                        {errors.main_heading.message}
                    </p>
                )}
            </div>

            <div>
                <label className="mb-1 block text-sm font-medium text-gray-700">
                    Sub Heading
                </label>

                <input
                    type="text"
                    placeholder="Sub heading (optional)"
                    className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                    {...register("sub_heading")}
                />
            </div>

            <div>
                <label className="mb-1 block text-sm font-medium text-gray-700">
                    Description
                </label>

                <textarea
                    rows={4}
                    placeholder="Description (optional)"
                    className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                    {...register("description")}
                />
            </div>

            <div>
                <label className="mb-1 block text-sm font-medium text-gray-700">
                    File
                </label>

                <input
                    ref={fileInputRef}
                    type="file"
                    accept=".pdf,.doc,.docx,.ppt,.pptx,.jpg,.jpeg,.png"
                    onChange={handleFileChange}
                    className="block w-full text-sm text-gray-600"
                />

                <p className="mt-1 text-xs text-gray-500">
                    Maximum size: 20 MB
                </p>

                {selectedFile && (
                    <p className="mt-1 text-sm text-gray-600">
                        Selected: {selectedFile.name}
                    </p>
                )}

                {fileError && (
                    <p className="mt-1 text-sm text-red-600">
                        {fileError}
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
                className="rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-60"
            >
                {isSubmitting ? "Uploading..." : "Upload Note"}
            </button>
        </form>
    );
}