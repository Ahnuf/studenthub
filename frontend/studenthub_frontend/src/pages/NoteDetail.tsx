import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import axios from "axios";

import {
    deleteNote,
    getNote,
} from "../api/notes";

import NoteEditForm from "../components/notes/NoteEditForm";

import type { Note } from "../types/notes";

interface ApiErrorResponse {
    success: boolean;
    message: string;
}

export default function NoteDetail() {
    const { noteId } = useParams();
    const navigate = useNavigate();

    const [note, setNote] = useState<Note | null>(null);
    const [isLoading, setIsLoading] = useState(true);
    const [isEditing, setIsEditing] = useState(false);
    const [isDeleting, setIsDeleting] = useState(false);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        if (!noteId) {
            return;
        }

        async function loadNote() {
            try {
                const data = await getNote(Number(noteId));
                setNote(data);
            } catch (err: unknown) {
                if (axios.isAxiosError<ApiErrorResponse>(err)) {
                    setError(
                        err.response?.data?.message ??
                            "Failed to load note.",
                    );
                } else {
                    setError("Failed to load note.");
                }
            } finally {
                setIsLoading(false);
            }
        }

        loadNote();
    }, [noteId]);

    async function handleDelete() {
        if (!note) {
            return;
        }

        const confirmed = window.confirm(
            "Are you sure you want to delete this note?",
        );

        if (!confirmed) {
            return;
        }

        setIsDeleting(true);
        setError(null);

        try {
            await deleteNote(note.id);
            navigate("/notes");
        } catch (err: unknown) {
            if (axios.isAxiosError<ApiErrorResponse>(err)) {
                setError(
                    err.response?.data?.message ??
                        "Failed to delete note.",
                );
            } else {
                setError("Failed to delete note.");
            }

            setIsDeleting(false);
        }
    }

    if (!noteId) {
        return (
            <div className="p-6">
                <div className="mx-auto max-w-3xl">
                    <p className="text-sm text-red-600">
                        Note not found.
                    </p>

                    <Link
                        to="/notes"
                        className="mt-4 inline-block text-sm text-blue-600 hover:underline"
                    >
                        Back to Notes
                    </Link>
                </div>
            </div>
        );
    }

    if (isLoading) {
        return (
            <div className="flex items-center justify-center py-24">
                <p className="text-gray-500">
                    Loading note...
                </p>
            </div>
        );
    }

    if (error && !note) {
        return (
            <div className="p-6">
                <div className="mx-auto max-w-3xl">
                    <p className="text-sm text-red-600">
                        {error}
                    </p>

                    <Link
                        to="/notes"
                        className="mt-4 inline-block text-sm text-blue-600 hover:underline"
                    >
                        Back to Notes
                    </Link>
                </div>
            </div>
        );
    }

    if (!note) {
        return null;
    }

    if (isEditing) {
        return (
            <div className="p-6">
                <div className="mx-auto max-w-3xl space-y-4">
                    <Link
                        to="/notes"
                        className="text-sm text-blue-600 hover:underline"
                    >
                        ← Back to Notes
                    </Link>

                    <NoteEditForm
                        note={note}
                        onUpdated={(updatedNote) => {
                            setNote(updatedNote);
                            setIsEditing(false);
                        }}
                        onCancel={() => setIsEditing(false)}
                    />
                </div>
            </div>
        );
    }

    return (
        <div className="p-6">
            <div className="mx-auto max-w-3xl space-y-6">
                <Link
                    to="/notes"
                    className="text-sm text-blue-600 hover:underline"
                >
                    ← Back to Notes
                </Link>

                <article className="rounded-lg bg-white p-6 shadow-sm">
                    <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
                        <div>
                            <h1 className="text-2xl font-semibold text-gray-900">
                                {note.main_heading}
                            </h1>

                            {note.sub_heading && (
                                <p className="mt-1 text-lg text-gray-600">
                                    {note.sub_heading}
                                </p>
                            )}

                            <p className="mt-2 text-sm text-gray-500">
                                {note.course_title}
                            </p>
                        </div>

                        <div className="flex gap-2">
                            <button
                                type="button"
                                onClick={() => setIsEditing(true)}
                                className="rounded-md border border-gray-300 px-3 py-1.5 text-sm font-medium text-gray-700 hover:bg-gray-50"
                            >
                                Edit
                            </button>

                            <button
                                type="button"
                                onClick={handleDelete}
                                disabled={isDeleting}
                                className="rounded-md bg-red-600 px-3 py-1.5 text-sm font-medium text-white hover:bg-red-700 disabled:opacity-60"
                            >
                                {isDeleting
                                    ? "Deleting..."
                                    : "Delete"}
                            </button>
                        </div>
                    </div>

                    {note.description && (
                        <div className="mt-6">
                            <h2 className="mb-2 font-semibold text-gray-900">
                                Description
                            </h2>

                            <p className="whitespace-pre-wrap text-sm leading-6 text-gray-700">
                                {note.description}
                            </p>
                        </div>
                    )}

                    <div className="mt-6 border-t border-gray-100 pt-4">
                        <p className="text-sm text-gray-500">
                            Uploaded by {note.uploaded_by}
                        </p>

                        <p className="mt-1 text-xs text-gray-400">
                            {new Date(
                                note.created_at,
                            ).toLocaleString()}
                        </p>
                    </div>

                    <a
                        href={note.file}
                        target="_blank"
                        rel="noreferrer"
                        className="mt-6 inline-block rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700"
                    >
                        Open File
                    </a>
                </article>

                {error && (
                    <p
                        className="text-sm text-red-600"
                        role="alert"
                    >
                        {error}
                    </p>
                )}
            </div>
        </div>
    );
}