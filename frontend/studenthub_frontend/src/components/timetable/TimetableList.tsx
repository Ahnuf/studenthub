import type { TimetableEntry } from "../../types/timetable";

interface TimetableListProps {
    entries: TimetableEntry[];
    onEdit: (entry: TimetableEntry) => void;
    onDelete: (entryId: number) => void;
    deletingId: number | null;
}

const DAY_ORDER = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
];

export default function TimetableList({
    entries,
    onEdit,
    onDelete,
    deletingId,
}: TimetableListProps) {
    const groupedEntries = [...entries].sort((a, b) => {
        if (a.day_of_week !== b.day_of_week) {
            return a.day_of_week - b.day_of_week;
        }

        return a.start_time.localeCompare(b.start_time);
    });

    return (
        <div className="space-y-4">
            {DAY_ORDER.map((day, dayIndex) => {
                const dayEntries = groupedEntries.filter(
                    (entry) => entry.day_of_week === dayIndex,
                );

                if (dayEntries.length === 0) {
                    return null;
                }

                return (
                    <section
                        key={day}
                        className="rounded-lg bg-white p-6 shadow-sm"
                    >
                        <h2 className="mb-4 text-lg font-semibold text-gray-900">
                            {day}
                        </h2>

                        <div className="space-y-3">
                            {dayEntries.map((entry) => (
                                <div
                                    key={entry.id}
                                    className="flex flex-col gap-3 rounded-md border border-gray-200 p-4 sm:flex-row sm:items-center sm:justify-between"
                                >
                                    <div>
                                        <p className="font-medium text-gray-900">
                                            {entry.course_name}
                                        </p>

                                        <p className="text-sm text-gray-600">
                                            {entry.start_time} — {entry.end_time}
                                        </p>

                                        {entry.location && (
                                            <p className="text-sm text-gray-500">
                                                {entry.location}
                                            </p>
                                        )}
                                    </div>

                                    <div className="flex gap-2">
                                        <button
                                            type="button"
                                            onClick={() => onEdit(entry)}
                                            className="rounded-md border border-gray-300 px-3 py-1.5 text-sm text-gray-700"
                                        >
                                            Edit
                                        </button>

                                        <button
                                            type="button"
                                            onClick={() => onDelete(entry.id)}
                                            disabled={deletingId === entry.id}
                                            className="rounded-md bg-red-600 px-3 py-1.5 text-sm text-white hover:bg-red-700 disabled:opacity-60"
                                        >
                                            {deletingId === entry.id
                                                ? "Deleting..."
                                                : "Delete"}
                                        </button>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </section>
                );
            })}

            {entries.length === 0 && (
                <div className="rounded-lg bg-white p-8 text-center shadow-sm">
                    <p className="text-sm text-gray-500">
                        Your timetable is empty.
                    </p>
                </div>
            )}
        </div>
    );
}