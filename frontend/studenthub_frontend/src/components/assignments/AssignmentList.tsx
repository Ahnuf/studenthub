import type { Assignment, AssignmentStatus } from "../../types/assignment";

interface Props {
    assignments: Assignment[];
    onStatusChange: (id: number, status: AssignmentStatus) => void;
    onDelete: (id: number) => void;
}

const STATUS_OPTIONS: AssignmentStatus[] = [
    "PENDING",
    "IN_PROGRESS",
    "COMPLETED",
];

function isOverdue(assignment: Assignment): boolean {
    if (assignment.status === "COMPLETED") return false;
    return new Date(assignment.due_date) < new Date(new Date().toDateString());
}

export default function AssignmentList({
    assignments,
    onStatusChange,
    onDelete,
}: Props) {
    if (assignments.length === 0) {
        return (
            <p className="rounded-lg bg-white p-6 text-center text-sm text-gray-500 shadow-sm">
                No assignments yet — add one above.
            </p>
        );
    }

    // Soonest due date first.
    const sorted = [...assignments].sort(
        (a, b) => new Date(a.due_date).getTime() - new Date(b.due_date).getTime(),
    );

    return (
        <div className="overflow-hidden rounded-lg bg-white shadow-sm">
            <ul className="divide-y divide-gray-100">
                {sorted.map((assignment) => {
                    const overdue = isOverdue(assignment);

                    return (
                        <li
                            key={assignment.id}
                            className="flex flex-wrap items-center justify-between gap-3 p-4"
                        >
                            <div>
                                <p className="font-medium text-gray-900">
                                    {assignment.title}
                                </p>
                                <p className="text-sm text-gray-500">
                                    {assignment.course_name} — due{" "}
                                    <span className={overdue ? "font-medium text-red-600" : ""}>
                                        {new Date(
                                            assignment.due_date,
                                        ).toLocaleDateString()}
                                        {overdue && " (overdue)"}
                                    </span>
                                </p>
                            </div>

                            <div className="flex items-center gap-2">
                                <select
                                    value={assignment.status}
                                    onChange={(e) =>
                                        onStatusChange(
                                            assignment.id,
                                            e.target.value as AssignmentStatus,
                                        )
                                    }
                                    className="rounded-md border border-gray-300 px-2 py-1 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                                >
                                    {STATUS_OPTIONS.map((status) => (
                                        <option key={status} value={status}>
                                            {status.replace("_", " ")}
                                        </option>
                                    ))}
                                </select>

                                <button
                                    onClick={() => onDelete(assignment.id)}
                                    className="rounded-md px-2 py-1 text-sm text-red-600 hover:bg-red-50"
                                >
                                    Delete
                                </button>
                            </div>
                        </li>
                    );
                })}
            </ul>
        </div>
    );
}
