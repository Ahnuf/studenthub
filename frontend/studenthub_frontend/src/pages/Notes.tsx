import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import axios from "axios";

import NoteForm from "../components/notes/NoteForm";
import { getCourses } from "../api/academic";
import { getNotes } from "../api/notes";

import type { Note } from "../types/notes";
import type { CourseOption } from "../api/academic";

interface ApiErrorResponse {
    success: boolean;
    message: string;
}

export default function Notes() {
    const [notes, setNotes] = useState<Note[]>([]);
    const [courses, setCourses] = useState<CourseOption[]>([]);

    const [searchQuery, setSearchQuery] = useState("");
    const [selectedCourse, setSelectedCourse] = useState<number | undefined>(
        undefined,
    );

    const [isLoading, setIsLoading] = useState(true);
    const [isSearching, setIsSearching] = useState(false);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        async function loadInitialData() {
            try {
                const [notesData, coursesData] = await Promise.all([
                    getNotes(),
                    getCourses(),
                ]);

                setNotes(notesData);
                setCourses(coursesData);
            } catch (err: unknown) {
                if (axios.isAxiosError<ApiErrorResponse>(err)) {
                    setError(
                        err.response?.data?.message ??
                            "Failed to load notes.",
                    );
                } else {
                    setError("Failed to load notes.");
                }
            } finally {
                setIsLoading(false);
            }
        }

        loadInitialData();
    }, []);

    async function loadNotes(
        query: string,
        courseId: number | undefined,
    ) {
        setError(null);
        setIsSearching(true);

        try {
            const data = await getNotes(courseId, query);
            setNotes(data);
        } catch (err: unknown) {
            if (axios.isAxiosError<ApiErrorResponse>(err)) {
                setError(
                    err.response?.data?.message ??
                        "Failed to search notes.",
                );
            } else {
                setError("Failed to search notes.");
            }
        } finally {
            setIsSearching(false);
        }
    }

    function handleSearchSubmit(
        event: React.FormEvent<HTMLFormElement>,
    ) {
        event.preventDefault();

        void loadNotes(
            searchQuery.trim(),
            selectedCourse,
        );
    }

    function handleCourseChange(
        event: React.ChangeEvent<HTMLSelectElement>,
    ) {
        const value = event.target.value;

        const courseId =
            value === "" ? undefined : Number(value);

        setSelectedCourse(courseId);

        void loadNotes(
            searchQuery.trim(),
            courseId,
        );
    }

    function handleCreated(note: Note) {
        setNotes((current) => [note, ...current]);
    }

    return (
        <div className="p-6">
            <div className="mx-auto max-w-5xl space-y-6">
                <div>
                    <h1 className="text-2xl font-semibold text-gray-900">
                        Notes
                    </h1>

                    <p className="mt-1 text-sm text-gray-500">
                        Upload and search your academic notes.
                    </p>
                </div>

                <NoteForm onCreated={handleCreated} />

                <section className="rounded-lg bg-white p-6 shadow-sm">
                    <div className="mb-4 flex flex-col gap-3 md:flex-row">
                        <form
                            onSubmit={handleSearchSubmit}
                            className="flex flex-1 gap-2"
                        >
                            <input
                                type="search"
                                value={searchQuery}
                                onChange={(event) =>
                                    setSearchQuery(event.target.value)
                                }
                                placeholder="Search notes..."
                                className="flex-1 rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                            />

                            <button
                                type="submit"
                                disabled={isSearching}
                                className="rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-60"
                            >
                                {isSearching ? "Searching..." : "Search"}
                            </button>
                        </form>

                        <select
                            value={selectedCourse ?? ""}
                            onChange={handleCourseChange}
                            className="rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                        >
                            <option value="">
                                All courses
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
                    </div>

                    {error && (
                        <p
                            className="mb-4 text-sm text-red-600"
                            role="alert"
                        >
                            {error}
                        </p>
                    )}

                    {isLoading ? (
                        <p className="text-sm text-gray-500">
                            Loading notes...
                        </p>
                    ) : notes.length === 0 ? (
                        <p className="text-sm text-gray-500">
                            No notes found.
                        </p>
                    ) : (
                        <div className="space-y-3">
                            {notes.map((note) => (
                                <Link
                                    key={note.id}
                                    to={`/notes/${note.id}`}
                                    className="block rounded-md border border-gray-200 p-4 transition hover:border-blue-300 hover:bg-blue-50"
                                >
                                    <p className="font-medium text-gray-900">
                                        {note.main_heading}
                                    </p>

                                    {note.sub_heading && (
                                        <p className="mt-1 text-sm text-gray-600">
                                            {note.sub_heading}
                                        </p>
                                    )}

                                    <p className="mt-1 text-sm text-gray-500">
                                        {note.course_title}
                                    </p>

                                    <p className="mt-1 text-xs text-gray-400">
                                        Uploaded by{" "}
                                        {note.uploaded_by}
                                    </p>
                                </Link>
                            ))}
                        </div>
                    )}
                </section>
            </div>
        </div>
    );
}