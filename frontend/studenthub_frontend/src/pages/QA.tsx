import { useEffect, useState } from "react";
import axios from "axios";

import { getCourses } from "../api/academic";
import { getQuestions } from "../api/qa";

import QuestionForm from "../components/qa/QuestionForm";
import QuestionList from "../components/qa/QuestionList";

import type { CourseOption } from "../api/academic";
import type { Question } from "../types/qa";

interface ApiErrorResponse {
    success: boolean;
    message: string;
}

export default function QA() {
    const [questions, setQuestions] = useState<Question[]>([]);
    const [courses, setCourses] = useState<CourseOption[]>([]);
    const [selectedCourse, setSelectedCourse] = useState<number | undefined>(
        undefined,
    );

    const [isLoading, setIsLoading] = useState(true);
    const [isFiltering, setIsFiltering] = useState(false);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        async function loadInitialData() {
            try {
                const [questionsData, coursesData] = await Promise.all([
                    getQuestions(),
                    getCourses(),
                ]);

                setQuestions(questionsData);
                setCourses(coursesData);
            } catch (err: unknown) {
                if (axios.isAxiosError<ApiErrorResponse>(err)) {
                    setError(
                        err.response?.data?.message ??
                            "Failed to load questions.",
                    );
                } else {
                    setError("Failed to load questions.");
                }
            } finally {
                setIsLoading(false);
            }
        }

        loadInitialData();
    }, []);

    async function handleCourseChange(
        event: React.ChangeEvent<HTMLSelectElement>,
    ) {
        const value = event.target.value;

        const courseId =
            value === "" ? undefined : Number(value);

        setSelectedCourse(courseId);
        setError(null);
        setIsFiltering(true);

        try {
            const data = await getQuestions(courseId);
            setQuestions(data);
        } catch (err: unknown) {
            if (axios.isAxiosError<ApiErrorResponse>(err)) {
                setError(
                    err.response?.data?.message ??
                        "Failed to load questions.",
                );
            } else {
                setError("Failed to load questions.");
            }
        } finally {
            setIsFiltering(false);
        }
    }

    function handleCreated(question: Question) {
        setQuestions((current) => [
            question,
            ...current,
        ]);
    }

    return (
        <div className="p-6">
            <div className="mx-auto max-w-5xl space-y-6">
                <div>
                    <h1 className="text-2xl font-semibold text-gray-900">
                        Q&amp;A
                    </h1>

                    <p className="mt-1 text-sm text-gray-500">
                        Ask questions and help other students.
                    </p>
                </div>

                <QuestionForm
                    onCreated={handleCreated}
                />

                <section className="rounded-lg bg-white p-4 shadow-sm">
                    <label className="mb-1 block text-sm font-medium text-gray-700">
                        Filter by course
                    </label>

                    <select
                        value={selectedCourse ?? ""}
                        onChange={handleCourseChange}
                        disabled={isFiltering}
                        className="w-full max-w-md rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 disabled:bg-gray-100"
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
                            Loading questions...
                        </p>
                    </div>
                ) : (
                    <QuestionList questions={questions} />
                )}
            </div>
        </div>
    );
}