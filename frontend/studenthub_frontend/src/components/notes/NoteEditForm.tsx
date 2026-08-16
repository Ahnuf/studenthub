"use no memo";

import { useRef, useState } from "react";
import { useForm } from "react-hook-form";
import axios from "axios";

import { updateNote } from "../../api/notes";

import type {
    Note,
    NoteUpdateRequest,
} from "../../types/notes";

interface ApiErrorResponse {
    success: boolean;
    message: string;
}

interface Props {
    note: Note;
    onUpdated: (note: Note) => void;
    onCancel: () => void;
}

interface NoteEditFormData {
    main_heading: string;
    sub_heading: string;
    description: string;
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

export default function NoteEditForm({
    note,
    onUpdated,
    onCancel,
}: Props) {
    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const [fileError, setFileError] = useState<string | null>(null);
    const [serverError, setServerError] = useState<string | null>(null);
    const [isSubmitting, setIsSubmitting] = useState(false);

    const fileInputRef = useRef<HTMLInputElement | null>(null);

    const {
        register,
        handleSubmit,
        formState: { errors },
    } = useForm<NoteEditFormData>({
        defaultValues: {
            main_heading: note.main_heading,
            sub_heading: note.sub_heading ?? "",
            description: note.description ?? "",
        },
    });

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

    async function onSubmit(data: NoteEditFormData) {
        setServerError(null);
        setFileError(null);
        setIsSubmitting(true);

        try {
            const payload: NoteUpdateRequest = {
                main_heading: data.main_heading,
                sub_heading: data.sub_heading,
                description: data.description,
            };

            if (selectedFile) {
                payload.file = selectedFile;
            }

            const updatedNote = await updateNote(
                note.id,
                payload,
            );

            onUpdated(updatedNote);
        } catch (err: unknown) {
            let message = "Failed to update note.";

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
                Edit Note
            </h2>

            <div>
                <label className="mb-1 block text-sm font-medium text-gray-700">
                    Main Heading
                </label>

                <input
                    type="text"
                    {...register("main_heading", {
                        required: "Main heading is required",
                    })}
                    className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
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
                    {...register("sub_heading")}
                    className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                />
            </div>

            <div>
                <label className="mb-1 block text-sm font-medium text-gray-700">
                    Description
                </label>

                <textarea
                    rows={4}
                    {...register("description")}
                    className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                />
            </div>

            <div>
                <label className="mb-1 block text-sm font-medium text-gray-700">
                    Replace File
                </label>

                <input
                    ref={fileInputRef}
                    type="file"
                    accept=".pdf,.doc,.docx,.ppt,.pptx,.jpg,.jpeg,.png"
                    onChange={handleFileChange}
                    className="block w-full text-sm text-gray-600"
                />

                <p className="mt-1 text-xs text-gray-500">
                    Leave empty to keep the existing file.
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

            <div className="flex gap-3">
                <button
                    type="submit"
                    disabled={isSubmitting}
                    className="rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-60"
                >
                    {isSubmitting ? "Saving..." : "Save Changes"}
                </button>

                <button
                    type="button"
                    onClick={onCancel}
                    disabled={isSubmitting}
                    className="rounded-md border border-gray-300 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-60"
                >
                    Cancel
                </button>
            </div>
        </form>
    );
}