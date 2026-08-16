import { useEffect, useState } from "react";
import axios from "axios";
import {
    listAssignments,
    updateAssignment,
    deleteAssignment,
} from "../api/assignments";
import type { Assignment, AssignmentStatus } from "../types/assignment";
import AssignmentForm from "../components/assignments/AssignmentForm";
import AssignmentList from "../components/assignments/AssignmentList";

interface ApiErrorResponse {
    success: boolean;
    message: string;
}

export default function Assignments() {
    const [assignments, setAssignments] = useState<Assignment[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        listAssignments()
            .then((res) => setAssignments(res.data))
            .catch(() => setError("Failed to load assignments."))
            .finally(() => setIsLoading(false));
    }, []);

    function handleCreated(assignment: Assignment) {
        setAssignments((prev) => [...prev, assignment]);
    }

    async function handleStatusChange(id: number, status: AssignmentStatus) {
        // Optimistic update -- reflect the change immediately,
        // roll back if the request actually fails.
        const previous = assignments;
        setAssignments((prev) =>
            prev.map((a) => (a.id === id ? { ...a, status } : a)),
        );

        try {
            await updateAssignment(id, { status });
        } catch (err: unknown) {
            setAssignments(previous);

            let message = "Failed to update status.";
            if (axios.isAxiosError<ApiErrorResponse>(err)) {
                message = err.response?.data?.message ?? message;
            }
            setError(message);
        }
    }

    async function handleDelete(id: number) {
        const previous = assignments;
        setAssignments((prev) => prev.filter((a) => a.id !== id));

        try {
            await deleteAssignment(id);
        } catch (err: unknown) {
            setAssignments(previous);

            let message = "Failed to delete assignment.";
            if (axios.isAxiosError<ApiErrorResponse>(err)) {
                message = err.response?.data?.message ?? message;
            }
            setError(message);
        }
    }

    if (isLoading) {
        return (
            <div className="flex items-center justify-center py-24">
                <p className="text-gray-500">Loading assignments...</p>
            </div>
        );
    }

    return (
        <div className="p-6">
            <div className="mx-auto max-w-3xl space-y-6">
                <h1 className="text-2xl font-semibold text-gray-900">
                    Assignments
                </h1>

                <AssignmentForm onCreated={handleCreated} />

                {error && (
                    <p className="text-sm text-red-600" role="alert">
                        {error}
                    </p>
                )}

                <AssignmentList
                    assignments={assignments}
                    onStatusChange={handleStatusChange}
                    onDelete={handleDelete}
                />
            </div>
        </div>
    );
}
