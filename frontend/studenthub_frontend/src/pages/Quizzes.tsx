import { useEffect, useState } from "react";
import axios from "axios";

import { getCourses } from "../api/academic";
import { getQuizzes } from "../api/quizzes";

import QuizList from "../components/quizzes/QuizList";

import type { CourseOption } from "../api/academic";
import type { Quiz } from "../types/quizzes";

interface ApiErrorResponse {
    success: boolean;
    message: string;
}

export default function Quizzes() {
    const [quizzes, setQuizzes] = useState<Quiz[]>([]);
    const [courses, setCourses] = useState<CourseOption[]>([]);

    const [searchQuery, setSearchQuery] = useState("");
    const [selectedCourse, setSelectedCourse] = useState<
        number | undefined
    >(undefined);

    const [isLoading, setIsLoading] = useState(true);
    const [isSearching, setIsSearching] = useState(false);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        async function loadInitialData() {
            try {
                const [quizzesData, coursesData] = await Promise.all([
                    getQuizzes(),
                    getCourses(),
                ]);

                setQuizzes(quizzesData);
                setCourses(coursesData);
            } catch (err: unknown) {
                if (axios.isAxiosError<ApiErrorResponse>(err)) {
                    setError(
                        err.response?.data?.message ??
                            "Failed to load quizzes.",
                    );
                } else {
                    setError("Failed to load quizzes.");
                }
            } finally {
                setIsLoading(false);
            }
        }

        loadInitialData();
    }, []);

    async function loadQuizzes(
        query: string,
        courseId: number | undefined,
    ) {
        setError(null);
        setIsSearching(true);

        try {
            const data = await getQuizzes(
                courseId,
                query,
            );

            setQuizzes(data);
        } catch (err: unknown) {
            if (axios.isAxiosError<ApiErrorResponse>(err)) {
                setError(
                    err.response?.data?.message ??
                        "Failed to load quizzes.",
                );
            } else {
                setError("Failed to load quizzes.");
            }
        } finally {
            setIsSearching(false);
        }
    }

    function handleSearchSubmit(
        event: React.FormEvent<HTMLFormElement>,
    ) {
        event.preventDefault();

        void loadQuizzes(
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

        void loadQuizzes(
            searchQuery.trim(),
            courseId,
        );
    }

    return (
        <div className="p-6">
            <div className="mx-auto max-w-5xl space-y-6">
                <div>
                    <h1 className="text-2xl font-semibold text-gray-900">
                        Quizzes
                    </h1>

                    <p className="mt-1 text-sm text-gray-500">
                        Test your knowledge with student-created quizzes.
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
                                placeholder="Search quizzes..."
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
                                    {course.course_code} —{" "}
                                    {course.title}
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
                            Loading quizzes...
                        </p>
                    </div>
                ) : (
                    <QuizList quizzes={quizzes} />
                )}
            </div>
        </div>
    );
}