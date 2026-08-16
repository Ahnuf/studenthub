import { useEffect } from "react";
import { useForm } from "react-hook-form";

import type {
    TimetableCreateRequest,
    TimetableEntry,
} from "../../types/timetable";

interface TimetableFormProps {
    editingEntry?: TimetableEntry | null;
    isSubmitting: boolean;
    onSubmit: (data: TimetableCreateRequest) => void;
    onCancelEdit: () => void;
}

interface TimetableFormData {
    course_name: string;
    day_of_week: number;
    start_time: string;
    end_time: string;
    location: string;
}

const DAYS = [
    { value: 0, label: "Monday" },
    { value: 1, label: "Tuesday" },
    { value: 2, label: "Wednesday" },
    { value: 3, label: "Thursday" },
    { value: 4, label: "Friday" },
    { value: 5, label: "Saturday" },
    { value: 6, label: "Sunday" },
];

export default function TimetableForm({
    editingEntry,
    isSubmitting,
    onSubmit,
    onCancelEdit,
}: TimetableFormProps) {
    const {
        register,
        handleSubmit,
        reset,
        formState: { errors },
    } = useForm<TimetableFormData>({
        defaultValues: {
            course_name: "",
            day_of_week: 0,
            start_time: "",
            end_time: "",
            location: "",
        },
    });

    useEffect(() => {
        if (editingEntry) {
            reset({
                course_name: editingEntry.course_name,
                day_of_week: editingEntry.day_of_week,
                start_time: editingEntry.start_time,
                end_time: editingEntry.end_time,
                location: editingEntry.location ?? "",
            });
        } else {
            reset({
                course_name: "",
                day_of_week: 0,
                start_time: "",
                end_time: "",
                location: "",
            });
        }
    }, [editingEntry, reset]);

    function handleFormSubmit(data: TimetableFormData) {
        onSubmit({
            course_name: data.course_name,
            day_of_week: Number(data.day_of_week),
            start_time: data.start_time,
            end_time: data.end_time,
            location: data.location,
        });
    }

    return (
        <form
            onSubmit={handleSubmit(handleFormSubmit)}
            className="space-y-4 rounded-lg bg-white p-6 shadow-sm"
        >
            <div>
                <label className="mb-1 block text-sm font-medium text-gray-700">
                    Course Name
                </label>

                <input
                    type="text"
                    {...register("course_name", {
                        required: "Course name is required",
                    })}
                    className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm"
                    placeholder="e.g. Database Systems"
                />

                {errors.course_name && (
                    <p className="mt-1 text-sm text-red-600">
                        {errors.course_name.message}
                    </p>
                )}
            </div>

            <div>
                <label className="mb-1 block text-sm font-medium text-gray-700">
                    Day
                </label>

                <select
                    {...register("day_of_week", {
                        valueAsNumber: true,
                    })}
                    className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm"
                >
                    {DAYS.map((day) => (
                        <option key={day.value} value={day.value}>
                            {day.label}
                        </option>
                    ))}
                </select>
            </div>

            <div className="grid gap-4 sm:grid-cols-2">
                <div>
                    <label className="mb-1 block text-sm font-medium text-gray-700">
                        Start Time
                    </label>

                    <input
                        type="time"
                        {...register("start_time", {
                            required: "Start time is required",
                        })}
                        className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm"
                    />

                    {errors.start_time && (
                        <p className="mt-1 text-sm text-red-600">
                            {errors.start_time.message}
                        </p>
                    )}
                </div>

                <div>
                    <label className="mb-1 block text-sm font-medium text-gray-700">
                        End Time
                    </label>

                    <input
                        type="time"
                        {...register("end_time", {
                            required: "End time is required",
                        })}
                        className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm"
                    />

                    {errors.end_time && (
                        <p className="mt-1 text-sm text-red-600">
                            {errors.end_time.message}
                        </p>
                    )}
                </div>
            </div>

            <div>
                <label className="mb-1 block text-sm font-medium text-gray-700">
                    Location
                </label>

                <input
                    type="text"
                    {...register("location")}
                    className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm"
                    placeholder="e.g. Lab 3"
                />
            </div>

            <div className="flex gap-3">
                <button
                    type="submit"
                    disabled={isSubmitting}
                    className="rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-60"
                >
                    {isSubmitting
                        ? "Saving..."
                        : editingEntry
                            ? "Update Entry"
                            : "Add to Timetable"}
                </button>

                {editingEntry && (
                    <button
                        type="button"
                        onClick={onCancelEdit}
                        className="rounded-md border border-gray-300 px-4 py-2 text-sm font-medium text-gray-700"
                    >
                        Cancel
                    </button>
                )}
            </div>
        </form>
    );
}