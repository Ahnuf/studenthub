import { useEffect, useState } from "react";
import axios from "axios";

import { getCourses } from "../api/academic";
import { getDecks } from "../api/flashcards";

import DeckList from "../components/flashcards/DeckList";

import type { CourseOption } from "../api/academic";
import type { FlashcardDeck } from "../types/flashcards";

interface ApiErrorResponse {
    success: boolean;
    message: string;
}

export default function Flashcards() {
    const [decks, setDecks] = useState<FlashcardDeck[]>([]);
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
                const [decksData, coursesData] = await Promise.all([
                    getDecks(),
                    getCourses(),
                ]);

                setDecks(decksData);
                setCourses(coursesData);
            } catch (err: unknown) {
                if (axios.isAxiosError<ApiErrorResponse>(err)) {
                    setError(
                        err.response?.data?.message ??
                            "Failed to load flashcard decks.",
                    );
                } else {
                    setError(
                        "Failed to load flashcard decks.",
                    );
                }
            } finally {
                setIsLoading(false);
            }
        }

        loadInitialData();
    }, []);

    async function loadDecks(
        query: string,
        courseId: number | undefined,
    ) {
        setError(null);
        setIsSearching(true);

        try {
            const data = await getDecks(courseId, query);
            setDecks(data);
        } catch (err: unknown) {
            if (axios.isAxiosError<ApiErrorResponse>(err)) {
                setError(
                    err.response?.data?.message ??
                        "Failed to load flashcard decks.",
                );
            } else {
                setError(
                    "Failed to load flashcard decks.",
                );
            }
        } finally {
            setIsSearching(false);
        }
    }

    function handleSearchSubmit(
        event: React.FormEvent<HTMLFormElement>,
    ) {
        event.preventDefault();

        void loadDecks(
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

        void loadDecks(
            searchQuery.trim(),
            courseId,
        );
    }

    return (
        <div className="p-6">
            <div className="mx-auto max-w-5xl space-y-6">
                <div>
                    <h1 className="text-2xl font-semibold text-gray-900">
                        Flashcards
                    </h1>

                    <p className="mt-1 text-sm text-gray-500">
                        Study shared flashcard decks for your courses.
                    </p>
                </div>

                <section className="rounded-lg bg-white p-6 shadow-sm">
                    <div className="flex flex-col gap-3 md:flex-row">
                        <form
                            onSubmit={handleSearchSubmit}
                            className="flex flex-1 gap-2"
                        >
                            <input
                                type="search"
                                value={searchQuery}
                                onChange={(event) =>
                                    setSearchQuery(
                                        event.target.value,
                                    )
                                }
                                placeholder="Search flashcard decks..."
                                className="flex-1 rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                            />

                            <button
                                type="submit"
                                disabled={isSearching}
                                className="rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-60"
                            >
                                {isSearching
                                    ? "Searching..."
                                    : "Search"}
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
                </section>

                {error && (
                    <p
                        className="text-sm text-red-600"
                        role="alert"
                    >
                        {error}
                    </p>
                )}

                {isLoading ? (
                    <div className="rounded-lg bg-white p-6 shadow-sm">
                        <p className="text-sm text-gray-500">
                            Loading flashcard decks...
                        </p>
                    </div>
                ) : (
                    <DeckList decks={decks} />
                )}
            </div>
        </div>
    );
}