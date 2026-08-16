import { useEffect, useState } from "react";
import axios from "axios";

import {
    createTimetableEntry,
    deleteTimetableEntry,
    getTimetable,
    updateTimetableEntry,
} from "../api/timetable";

import TimetableForm from "../components/timetable/TimetableForm";
import TimetableList from "../components/timetable/TimetableList";

import type {
    TimetableCreateRequest,
    TimetableEntry,
} from "../types/timetable";

interface ApiErrorResponse {
    success: boolean;
    message: string;
}

export default function Timetable() {
    const [entries, setEntries] = useState<TimetableEntry[]>([]);
    const [editingEntry, setEditingEntry] = useState<TimetableEntry | null>(
        null,
    );

    const [isLoading, setIsLoading] = useState(true);
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [deletingId, setDeletingId] = useState<number | null>(null);

    const [serverError, setServerError] = useState<string | null>(null);
    const [warnings, setWarnings] = useState<string[]>([]);

    useEffect(() => {
        async function loadTimetable() {
            try {
                const data = await getTimetable();
                setEntries(data);
            } catch (err: unknown) {
                if (axios.isAxiosError<ApiErrorResponse>(err)) {
                    setServerError(
                        err.response?.data?.message ??
                            "Failed to load timetable.",
                    );
                } else {
                    setServerError("Failed to load timetable.");
                }
            } finally {
                setIsLoading(false);
            }
        }

        loadTimetable();
    }, []);

    async function handleSubmit(data: TimetableCreateRequest) {
        setServerError(null);
        setWarnings([]);
        setIsSubmitting(true);

        try {
            if (editingEntry) {
                const updatedEntry = await updateTimetableEntry(
                    editingEntry.id,
                    data,
                );

                setEntries((current) =>
                    current.map((entry) =>
                        entry.id === updatedEntry.id
                            ? updatedEntry
                            : entry,
                    ),
                );

                setEditingEntry(null);
            } else {
                const response = await createTimetableEntry(data);

                setEntries((current) => [
                    ...current,
                    response.data,
                ]);

                setWarnings(
                    response.warnings?.map((warning) => warning.message) ?? [],
                );
            }
        } catch (err: unknown) {
            if (axios.isAxiosError<ApiErrorResponse>(err)) {
                setServerError(
                    err.response?.data?.message ??
                        "Failed to save timetable entry.",
                );
            } else {
                setServerError("Failed to save timetable entry.");
            }
        } finally {
            setIsSubmitting(false);
        }
    }

    async function handleDelete(entryId: number) {
        setServerError(null);

        const previousEntries = entries;

        setEntries((current) =>
            current.filter((entry) => entry.id !== entryId),
        );

        setDeletingId(entryId);

        try {
            await deleteTimetableEntry(entryId);
        } catch (err: unknown) {
            setEntries(previousEntries);

            if (axios.isAxiosError<ApiErrorResponse>(err)) {
                setServerError(
                    err.response?.data?.message ??
                        "Failed to delete timetable entry.",
                );
            } else {
                setServerError("Failed to delete timetable entry.");
            }
        } finally {
            setDeletingId(null);
        }
    }

    if (isLoading) {
        return (
            <div className="flex items-center justify-center py-24">
                <p className="text-gray-500">
                    Loading your timetable...
                </p>
            </div>
        );
    }

    return (
        <div className="p-6">
            <div className="mx-auto max-w-5xl space-y-6">
                <div>
                    <h1 className="text-2xl font-semibold text-gray-900">
                        Timetable
                    </h1>

                    <p className="mt-1 text-sm text-gray-500">
                        Manage your weekly class schedule.
                    </p>
                </div>

                <TimetableForm
                    editingEntry={editingEntry}
                    isSubmitting={isSubmitting}
                    onSubmit={handleSubmit}
                    onCancelEdit={() => setEditingEntry(null)}
                />

                {warnings.length > 0 && (
                    <div className="rounded-lg border border-yellow-300 bg-yellow-50 p-4">
                        <p className="mb-2 font-medium text-yellow-900">
                            Timetable warnings
                        </p>

                        <ul className="list-disc space-y-1 pl-5 text-sm text-yellow-800">
                            {warnings.map((warning, index) => (
                                <li key={index}>{warning}</li>
                            ))}
                        </ul>
                    </div>
                )}

                {serverError && (
                    <p
                        className="text-sm text-red-600"
                        role="alert"
                    >
                        {serverError}
                    </p>
                )}

                <TimetableList
                    entries={entries}
                    onEdit={setEditingEntry}
                    onDelete={handleDelete}
                    deletingId={deletingId}
                />
            </div>
        </div>
    );
}