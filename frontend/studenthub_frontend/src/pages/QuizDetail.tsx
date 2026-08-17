"use no memo";

import { useEffect, useState } from "react";
import {
    Link,
    useNavigate,
    useParams,
} from "react-router-dom";
import axios from "axios";

import {
    deleteQuiz,
    deleteQuizQuestion,
    getQuiz,
    getQuizAttempts,
    getQuizQuestionForCreator,
    getQuizQuestions,
    submitQuizAttempt,
} from "../api/quizzes";

import QuizForm from "../components/quizzes/QuizForm";
import QuizQuestionCard from "../components/quizzes/QuizQuestionCard";
import QuizQuestionForm from "../components/quizzes/QuizQuestionForm";
import AttemptHistory from "../components/quizzes/AttemptHistory";

import type {
    Quiz,
    QuizAttempt,
    QuizQuestion,
    QuizQuestionCreator,
} from "../types/quizzes";

interface ApiErrorResponse {
    success: boolean;
    message: string;
}

export default function QuizDetail() {
    const { quizId } = useParams();
    const navigate = useNavigate();

    const [quiz, setQuiz] = useState<Quiz | null>(null);
    const [questions, setQuestions] = useState<QuizQuestion[]>([]);
    const [attempts, setAttempts] = useState<QuizAttempt[]>([]);

    const [answers, setAnswers] = useState<
        Record<number, number | null>
    >({});

    const [editingQuiz, setEditingQuiz] = useState(false);

    const [editingQuestion, setEditingQuestion] =
        useState<QuizQuestionCreator | null>(null);

    const [isLoading, setIsLoading] = useState(true);
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [isDeletingQuiz, setIsDeletingQuiz] = useState(false);

    const [deletingQuestionId, setDeletingQuestionId] =
        useState<number | null>(null);

    const [error, setError] = useState<string | null>(null);

    const [attemptResult, setAttemptResult] =
        useState<QuizAttempt | null>(null);

    useEffect(() => {
        if (!quizId) {
            return;
        }

        async function loadQuiz() {
            try {
                const id = Number(quizId);

                const [
                    quizData,
                    questionData,
                    attemptData,
                ] = await Promise.all([
                    getQuiz(id),
                    getQuizQuestions(id),
                    getQuizAttempts(id),
                ]);

                setQuiz(quizData);
                setQuestions(questionData);
                setAttempts(attemptData);
            } catch (err: unknown) {
                if (axios.isAxiosError<ApiErrorResponse>(err)) {
                    setError(
                        err.response?.data?.message ??
                            "Failed to load quiz.",
                    );
                } else {
                    setError("Failed to load quiz.");
                }
            } finally {
                setIsLoading(false);
            }
        }

        loadQuiz();
    }, [quizId]);

    function handleSelect(
        questionId: number,
        choiceId: number | null,
    ) {
        setAnswers((current) => ({
            ...current,
            [questionId]: choiceId,
        }));
    }

    async function handleSubmit() {
        if (!quiz) {
            return;
        }

        const submittedAnswers = questions.map(
            (question) => ({
                question_id: question.id,
                choice_id:
                    answers[question.id] === undefined
                        ? null
                        : answers[question.id],
            }),
        );

        setError(null);
        setIsSubmitting(true);

        try {
            const result = await submitQuizAttempt(
                quiz.id,
                {
                    answers: submittedAnswers,
                },
            );

            setAttemptResult(result);

            setAttempts((current) => [
                result,
                ...current,
            ]);

            setQuiz((current) => {
                if (!current) {
                    return current;
                }

                const attemptsRemaining = Math.max(
                    current.attempts_remaining - 1,
                    0,
                );

                return {
                    ...current,
                    attempts_used:
                        current.attempts_used + 1,
                    attempts_remaining:
                        attemptsRemaining,
                    can_attempt:
                        attemptsRemaining > 0,
                };
            });
        } catch (err: unknown) {
            if (axios.isAxiosError<ApiErrorResponse>(err)) {
                setError(
                    err.response?.data?.message ??
                        "Failed to submit quiz.",
                );
            } else {
                setError("Failed to submit quiz.");
            }
        } finally {
            setIsSubmitting(false);
        }
    }

    function handleQuizCreated(
        createdQuiz: Quiz,
    ) {
        setQuiz(createdQuiz);
        setEditingQuiz(false);
    }

    function handleQuizUpdated(
        updatedQuiz: Quiz,
    ) {
        setQuiz(updatedQuiz);
        setEditingQuiz(false);
    }

    async function handleDeleteQuiz() {
        if (!quiz) {
            return;
        }

        const confirmed = window.confirm(
            `Are you sure you want to delete "${quiz.title}"? This will also remove its questions.`,
        );

        if (!confirmed) {
            return;
        }

        setIsDeletingQuiz(true);
        setError(null);

        try {
            await deleteQuiz(quiz.id);
            navigate("/quizzes");
        } catch (err: unknown) {
            if (axios.isAxiosError<ApiErrorResponse>(err)) {
                setError(
                    err.response?.data?.message ??
                        "Failed to delete quiz.",
                );
            } else {
                setError(
                    "Failed to delete quiz.",
                );
            }

            setIsDeletingQuiz(false);
        }
    }

    function handleQuestionCreated(
        question: QuizQuestion,
    ) {
        setQuestions((current) =>
            [...current, question].sort(
                (a, b) =>
                    a.order - b.order ||
                    a.id - b.id,
            ),
        );
    }

    function handleQuestionUpdated(
        question: QuizQuestion,
    ) {
        setQuestions((current) =>
            current
                .map((item) =>
                    item.id === question.id
                        ? question
                        : item,
                )
                .sort(
                    (a, b) =>
                        a.order - b.order ||
                        a.id - b.id,
                ),
        );

        setEditingQuestion(null);
    }

    async function handleEditQuestion(
        question: QuizQuestion,
    ) {
        setError(null);

        try {
            const creatorQuestion =
                await getQuizQuestionForCreator(
                    question.id,
                );

            setEditingQuestion(
                creatorQuestion,
            );
        } catch (err: unknown) {
            if (axios.isAxiosError<ApiErrorResponse>(err)) {
                setError(
                    err.response?.data?.message ??
                        "Failed to load question for editing.",
                );
            } else {
                setError(
                    "Failed to load question for editing.",
                );
            }
        }
    }

    async function handleDeleteQuestion(
        question: QuizQuestion,
    ) {
        const confirmed = window.confirm(
            "Are you sure you want to delete this question?",
        );

        if (!confirmed) {
            return;
        }

        setDeletingQuestionId(
            question.id,
        );
        setError(null);

        try {
            await deleteQuizQuestion(
                question.id,
            );

            setQuestions((current) =>
                current.filter(
                    (item) =>
                        item.id !== question.id,
                ),
            );

            if (
                editingQuestion?.id ===
                question.id
            ) {
                setEditingQuestion(null);
            }
        } catch (err: unknown) {
            if (axios.isAxiosError<ApiErrorResponse>(err)) {
                setError(
                    err.response?.data?.message ??
                        "Failed to delete question.",
                );
            } else {
                setError(
                    "Failed to delete question.",
                );
            }
        } finally {
            setDeletingQuestionId(null);
        }
    }

    if (!quizId) {
        return (
            <div className="p-6">
                <div className="mx-auto max-w-4xl">
                    <p className="text-sm text-red-600">
                        Quiz not found.
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
                    Loading quiz...
                </p>
            </div>
        );
    }

    if (error && !quiz) {
        return (
            <div className="p-6">
                <div className="mx-auto max-w-4xl">
                    <p className="text-sm text-red-600">
                        {error}
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

    if (!quiz) {
        return null;
    }

    if (editingQuiz) {
        return (
            <div className="p-6">
                <div className="mx-auto max-w-4xl space-y-6">
                    <Link
                        to={`/quizzes/${quiz.id}`}
                        className="text-sm text-blue-600 hover:underline"
                    >
                        ← Back to Quiz
                    </Link>

                    <QuizForm
                        editingQuiz={quiz}
                        onCreated={handleQuizCreated}
                        onUpdated={handleQuizUpdated}
                        onCancelEdit={() =>
                            setEditingQuiz(false)
                        }
                    />
                </div>
            </div>
        );
    }

    if (attemptResult) {
        return (
            <div className="p-6">
                <div className="mx-auto max-w-4xl space-y-6">
                    <Link
                        to="/quizzes"
                        className="text-sm text-blue-600 hover:underline"
                    >
                        ← Back to Quizzes
                    </Link>

                    <section className="rounded-lg bg-white p-8 text-center shadow-sm">
                        <h1 className="text-2xl font-semibold text-gray-900">
                            Quiz Complete
                        </h1>

                        <p className="mt-4 text-4xl font-bold text-blue-600">
                            {
                                attemptResult.score_percentage
                            }
                            %
                        </p>

                        <p className="mt-2 text-sm text-gray-500">
                            {
                                attemptResult.correct_answers
                            }{" "}
                            /{" "}
                            {
                                attemptResult.total_questions
                            }{" "}
                            correct
                        </p>

                        <p className="mt-4 text-sm text-gray-500">
                            Attempts remaining:{" "}
                            {
                                quiz.attempts_remaining
                            }
                        </p>

                        <div className="mt-6 flex justify-center gap-3">
                            <Link
                                to={`/quizzes/attempts/${attemptResult.id}`}
                                className="rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700"
                            >
                                Review Result
                            </Link>

                            <Link
                                to="/quizzes"
                                className="rounded-md border border-gray-300 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
                            >
                                Back to Quizzes
                            </Link>
                        </div>
                    </section>
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
                    <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
                        <div>
                            <p className="text-sm text-gray-500">
                                {quiz.course_title}
                            </p>

                            <h1 className="mt-1 text-2xl font-semibold text-gray-900">
                                {quiz.title}
                            </h1>

                            {quiz.description && (
                                <p className="mt-2 text-sm leading-6 text-gray-600">
                                    {quiz.description}
                                </p>
                            )}

                            <p className="mt-3 text-xs text-gray-400">
                                Created by{" "}
                                {quiz.created_by}
                            </p>
                        </div>

                        <div className="flex flex-col items-end gap-3">
                            <div className="rounded-lg bg-gray-50 px-4 py-3 text-sm text-gray-600">
                                <p>
                                    {
                                        quiz.attempts_remaining
                                    }{" "}
                                    {quiz.attempts_remaining ===
                                    1
                                        ? "attempt"
                                        : "attempts"}{" "}
                                    remaining
                                </p>
                            </div>

                            {quiz.is_creator && (
                                <div className="flex gap-2">
                                    <button
                                        type="button"
                                        onClick={() =>
                                            setEditingQuiz(
                                                true,
                                            )
                                        }
                                        className="rounded-md border border-gray-300 px-3 py-1.5 text-sm font-medium text-gray-700 hover:bg-gray-50"
                                    >
                                        Edit Quiz
                                    </button>

                                    <button
                                        type="button"
                                        onClick={() =>
                                            void handleDeleteQuiz()
                                        }
                                        disabled={
                                            isDeletingQuiz
                                        }
                                        className="rounded-md bg-red-600 px-3 py-1.5 text-sm font-medium text-white hover:bg-red-700 disabled:opacity-60"
                                    >
                                        {isDeletingQuiz
                                            ? "Deleting..."
                                            : "Delete Quiz"}
                                    </button>
                                </div>
                            )}
                        </div>
                    </div>
                </section>

                {!quiz.is_creator && (
                    <section className="space-y-3">
                        <h2 className="text-lg font-semibold text-gray-900">
                            Your Attempts
                        </h2>

                        <AttemptHistory
                            attempts={attempts}
                        />
                    </section>
                )}

                {quiz.is_creator && (
                    <QuizQuestionForm
                        quizId={quiz.id}
                        editingQuestion={
                            editingQuestion
                        }
                        nextOrder={
                            questions.length > 0
                                ? Math.max(
                                      ...questions.map(
                                          (question) =>
                                              question.order,
                                      ),
                                  ) + 1
                                : 0
                        }
                        onCreated={
                            handleQuestionCreated
                        }
                        onUpdated={
                            handleQuestionUpdated
                        }
                        onCancelEdit={() =>
                            setEditingQuestion(
                                null,
                            )
                        }
                    />
                )}

                {error && (
                    <p
                        className="text-sm text-red-600"
                        role="alert"
                    >
                        {error}
                    </p>
                )}

                {questions.length === 0 ? (
                    <section className="rounded-lg bg-white p-6 shadow-sm">
                        <p className="text-sm text-gray-500">
                            This quiz has no questions yet.
                        </p>
                    </section>
                ) : quiz.is_creator ? (
                    <section className="space-y-4">
                        <h2 className="text-lg font-semibold text-gray-900">
                            Questions
                        </h2>

                        {questions.map(
                            (question) => (
                                <div
                                    key={
                                        question.id
                                    }
                                    className="space-y-2"
                                >
                                    <QuizQuestionCard
                                        question={
                                            question
                                        }
                                        selectedChoiceId={
                                            null
                                        }
                                        onSelect={() =>
                                            undefined
                                        }
                                    />

                                    <div className="flex justify-end gap-2">
                                        <button
                                            type="button"
                                            onClick={() =>
                                                void handleEditQuestion(
                                                    question,
                                                )
                                            }
                                            className="rounded-md border border-gray-300 px-3 py-1.5 text-sm text-gray-700 hover:bg-gray-50"
                                        >
                                            Edit
                                        </button>

                                        <button
                                            type="button"
                                            onClick={() =>
                                                void handleDeleteQuestion(
                                                    question,
                                                )
                                            }
                                            disabled={
                                                deletingQuestionId ===
                                                question.id
                                            }
                                            className="rounded-md bg-red-600 px-3 py-1.5 text-sm text-white hover:bg-red-700 disabled:opacity-60"
                                        >
                                            {deletingQuestionId ===
                                            question.id
                                                ? "Deleting..."
                                                : "Delete"}
                                        </button>
                                    </div>
                                </div>
                            ),
                        )}
                    </section>
                ) : !quiz.can_attempt ? (
                    <section className="rounded-lg bg-white p-6 shadow-sm">
                        <p className="text-sm text-gray-600">
                            You have used all 5 attempts for this quiz.
                        </p>
                    </section>
                ) : (
                    <section className="space-y-4">
                        {questions.map(
                            (question) => (
                                <QuizQuestionCard
                                    key={
                                        question.id
                                    }
                                    question={
                                        question
                                    }
                                    selectedChoiceId={
                                        answers[
                                            question
                                                .id
                                        ] ??
                                        null
                                    }
                                    onSelect={
                                        handleSelect
                                    }
                                />
                            ),
                        )}

                        <div className="flex justify-end">
                            <button
                                type="button"
                                onClick={() =>
                                    void handleSubmit()
                                }
                                disabled={
                                    isSubmitting
                                }
                                className="rounded-md bg-blue-600 px-5 py-2.5 text-sm font-medium text-white hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-60"
                            >
                                {isSubmitting
                                    ? "Submitting..."
                                    : "Submit Quiz"}
                            </button>
                        </div>
                    </section>
                )}
            </div>
        </div>
    );
}