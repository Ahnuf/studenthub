import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import axios from "axios";

import { getQuizAttempt } from "../api/quizzes";

import type { QuizAttempt } from "../types/quizzes";

interface ApiErrorResponse {
    success: boolean;
    message: string;
}

export default function QuizAttemptReview() {
    const { attemptId } = useParams();

    const [attempt, setAttempt] = useState<QuizAttempt | null>(
        null,
    );
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        if (!attemptId) {
            return;
        }

        async function loadAttempt() {
            try {
                const data = await getQuizAttempt(
                    Number(attemptId),
                );

                setAttempt(data);
            } catch (err: unknown) {
                if (axios.isAxiosError<ApiErrorResponse>(err)) {
                    setError(
                        err.response?.data?.message ??
                            "Failed to load attempt.",
                    );
                } else {
                    setError("Failed to load attempt.");
                }
            } finally {
                setIsLoading(false);
            }
        }

        loadAttempt();
    }, [attemptId]);

    if (!attemptId) {
        return (
            <div className="p-6">
                <div className="mx-auto max-w-4xl">
                    <p className="text-sm text-red-600">
                        Attempt not found.
                    </p>

                    <Link
                        to="/quizzes"
                        className="mt-4 inline-block text-sm text-blue-600 hover:underline"
                    >
                        Back to Quizzes
                    </Link>
                </div>
            </div>
        );
    }

    if (isLoading) {
        return (
            <div className="flex items-center justify-center py-24">
                <p className="text-gray-500">
                    Loading attempt...
                </p>
            </div>
        );
    }

    if (error || !attempt) {
        return (
            <div className="p-6">
                <div className="mx-auto max-w-4xl">
                    <p className="text-sm text-red-600">
                        {error ?? "Attempt not found."}
                    </p>

                    <Link
                        to="/quizzes"
                        className="mt-4 inline-block text-sm text-blue-600 hover:underline"
                    >
                        Back to Quizzes
                    </Link>
                </div>
            </div>
        );
    }

    return (
        <div className="p-6">
            <div className="mx-auto max-w-4xl space-y-6">
                <Link
                    to="/quizzes"
                    className="text-sm text-blue-600 hover:underline"
                >
                    ← Back to Quizzes
                </Link>

                <section className="rounded-lg bg-white p-6 shadow-sm">
                    <h1 className="text-2xl font-semibold text-gray-900">
                        Quiz Result
                    </h1>

                    <div className="mt-6 grid gap-4 sm:grid-cols-3">
                        <div className="rounded-lg bg-gray-50 p-4 text-center">
                            <p className="text-xs text-gray-500">
                                Score
                            </p>

                            <p className="mt-1 text-3xl font-bold text-blue-600">
                                {attempt.score_percentage}%
                            </p>
                        </div>

                        <div className="rounded-lg bg-gray-50 p-4 text-center">
                            <p className="text-xs text-gray-500">
                                Correct
                            </p>

                            <p className="mt-1 text-2xl font-semibold text-gray-900">
                                {attempt.correct_answers} /{" "}
                                {attempt.total_questions}
                            </p>
                        </div>

                        <div className="rounded-lg bg-gray-50 p-4 text-center">
                            <p className="text-xs text-gray-500">
                                Completed
                            </p>

                            <p className="mt-1 text-sm font-medium text-gray-900">
                                {new Date(
                                    attempt.created_at,
                                ).toLocaleString()}
                            </p>
                        </div>
                    </div>
                </section>

                <section>
                    <h2 className="mb-3 text-lg font-semibold text-gray-900">
                        Answer Review
                    </h2>

                    <div className="space-y-4">
                        {attempt.answers.map((answer, index) => (
                            <article
                                key={answer.question_id}
                                className={`rounded-lg border bg-white p-6 shadow-sm ${
                                    answer.is_correct
                                        ? "border-green-300"
                                        : "border-red-300"
                                }`}
                            >
                                <div className="flex items-start justify-between gap-4">
                                    <h3 className="font-medium text-gray-900">
                                        {index + 1}.{" "}
                                        {answer.question_text}
                                    </h3>

                                    <span
                                        className={`shrink-0 rounded-full px-2.5 py-1 text-xs font-medium ${
                                            answer.is_correct
                                                ? "bg-green-100 text-green-700"
                                                : "bg-red-100 text-red-700"
                                        }`}
                                    >
                                        {answer.is_correct
                                            ? "Correct"
                                            : "Incorrect"}
                                    </span>
                                </div>

                                <div className="mt-4 space-y-2">
                                    {answer.choices.map((choice) => {
                                        const isSelected =
                                            answer.selected_choice_id ===
                                            choice.id;

                                        return (
                                            <div
                                                key={choice.id}
                                                className={`rounded-md border p-3 text-sm ${
                                                    choice.is_correct
                                                        ? "border-green-300 bg-green-50 text-green-800"
                                                        : isSelected
                                                          ? "border-red-300 bg-red-50 text-red-800"
                                                          : "border-gray-200 text-gray-700"
                                                }`}
                                            >
                                                <div className="flex items-center justify-between gap-3">
                                                    <span>
                                                        {choice.text}
                                                    </span>

                                                    <span className="text-xs font-medium">
                                                        {choice.is_correct
                                                            ? "Correct answer"
                                                            : isSelected
                                                              ? "Your answer"
                                                              : ""}
                                                    </span>
                                                </div>
                                            </div>
                                        );
                                    })}
                                </div>
                            </article>
                        ))}
                    </div>
                </section>
            </div>
        </div>
    );
}