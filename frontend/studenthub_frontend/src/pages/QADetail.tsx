import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import axios from "axios";

import {
    acceptAnswer,
    getQuestion,
    moderateAnswer,
    moderateQuestion,
    toggleAnswerVote,
} from "../api/qa";

import AnswerForm from "../components/qa/AnswerForm";
import AnswerList from "../components/qa/AnswerList";

import type {
    Answer,
    QuestionDetailData,
} from "../types/qa";

interface ApiErrorResponse {
    success: boolean;
    message: string;
}

export default function QADetail() {
    const { questionId } = useParams();

    const [data, setData] = useState<QuestionDetailData | null>(
        null,
    );
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const [isVoting, setIsVoting] = useState<number | null>(null);
    const [isAccepting, setIsAccepting] = useState<number | null>(
        null,
    );
    const [isModeratingQuestion, setIsModeratingQuestion] =
        useState(false);
    const [isModeratingAnswer, setIsModeratingAnswer] =
        useState<number | null>(null);

    useEffect(() => {
        if (!questionId) {
            return;
        }

        async function loadQuestion() {
            try {
                const result = await getQuestion(
                    Number(questionId),
                );

                setData(result);
            } catch (err: unknown) {
                if (axios.isAxiosError<ApiErrorResponse>(err)) {
                    setError(
                        err.response?.data?.message ??
                            "Failed to load question.",
                    );
                } else {
                    setError("Failed to load question.");
                }
            } finally {
                setIsLoading(false);
            }
        }

        loadQuestion();
    }, [questionId]);

    function handleAnswerCreated(answer: Answer) {
        setData((current) => {
            if (!current) {
                return current;
            }

            return {
                ...current,
                answers: [answer, ...current.answers],
                question: {
                    ...current.question,
                    answer_count:
                        current.question.answer_count + 1,
                },
            };
        });
    }

    async function handleVote(answer: Answer) {
        setIsVoting(answer.id);
        setError(null);

        try {
            const result = await toggleAnswerVote(answer.id);

            setData((current) => {
                if (!current) {
                    return current;
                }

                return {
                    ...current,
                    answers: current.answers.map((item) =>
                        item.id === answer.id
                            ? {
                                  ...item,
                                  has_voted:
                                      result.has_voted,
                                  vote_count:
                                      result.vote_count,
                              }
                            : item,
                    ),
                };
            });
        } catch (err: unknown) {
            if (axios.isAxiosError<ApiErrorResponse>(err)) {
                setError(
                    err.response?.data?.message ??
                        "Failed to update vote.",
                );
            } else {
                setError("Failed to update vote.");
            }
        } finally {
            setIsVoting(null);
        }
    }

    async function handleAccept(answer: Answer) {
        setIsAccepting(answer.id);
        setError(null);

        try {
            const acceptedAnswer = await acceptAnswer(answer.id);

            setData((current) => {
                if (!current) {
                    return current;
                }

                return {
                    ...current,
                    question: {
                        ...current.question,
                        is_resolved: true,
                    },
                    answers: current.answers.map((item) => ({
                        ...item,
                        is_accepted:
                            item.id === acceptedAnswer.id,
                    })),
                };
            });
        } catch (err: unknown) {
            if (axios.isAxiosError<ApiErrorResponse>(err)) {
                setError(
                    err.response?.data?.message ??
                        "Failed to accept answer.",
                );
            } else {
                setError("Failed to accept answer.");
            }
        } finally {
            setIsAccepting(null);
        }
    }

    async function handleModerateQuestion() {
        if (!data) {
            return;
        }

        setIsModeratingQuestion(true);
        setError(null);

        try {
            const updatedQuestion =
                await moderateQuestion(
                    data.question.id,
                    {
                        is_active: false,
                    },
                );

            setData((current) => {
                if (!current) {
                    return current;
                }

                return {
                    ...current,
                    question: {
                        ...current.question,
                        ...updatedQuestion,
                    },
                };
            });
        } catch (err: unknown) {
            if (axios.isAxiosError<ApiErrorResponse>(err)) {
                setError(
                    err.response?.data?.message ??
                        "Failed to moderate question.",
                );
            } else {
                setError("Failed to moderate question.");
            }
        } finally {
            setIsModeratingQuestion(false);
        }
    }

    async function handleModerateAnswer(answer: Answer) {
        setIsModeratingAnswer(answer.id);
        setError(null);

        try {
            await moderateAnswer(answer.id, {
                is_active: false,
            });

            setData((current) => {
                if (!current) {
                    return current;
                }

                return {
                    ...current,
                    answers: current.answers.filter(
                        (item) => item.id !== answer.id,
                    ),
                };
            });
        } catch (err: unknown) {
            if (axios.isAxiosError<ApiErrorResponse>(err)) {
                setError(
                    err.response?.data?.message ??
                        "Failed to moderate answer.",
                );
            } else {
                setError("Failed to moderate answer.");
            }
        } finally {
            setIsModeratingAnswer(null);
        }
    }

    if (!questionId) {
        return (
            <div className="p-6">
                <div className="mx-auto max-w-4xl">
                    <p className="text-sm text-red-600">
                        Question not found.
                    </p>

                    <Link
                        to="/qa"
                        className="mt-4 inline-block text-sm text-blue-600 hover:underline"
                    >
                        Back to Q&amp;A
                    </Link>
                </div>
            </div>
        );
    }

    if (isLoading) {
        return (
            <div className="flex items-center justify-center py-24">
                <p className="text-gray-500">
                    Loading question...
                </p>
            </div>
        );
    }

    if (error && !data) {
        return (
            <div className="p-6">
                <div className="mx-auto max-w-4xl">
                    <p className="text-sm text-red-600">
                        {error}
                    </p>

                    <Link
                        to="/qa"
                        className="mt-4 inline-block text-sm text-blue-600 hover:underline"
                    >
                        Back to Q&amp;A
                    </Link>
                </div>
            </div>
        );
    }

    if (!data) {
        return null;
    }

    return (
        <div className="p-6">
            <div className="mx-auto max-w-4xl space-y-6">
                <Link
                    to="/qa"
                    className="text-sm text-blue-600 hover:underline"
                >
                    ← Back to Q&amp;A
                </Link>

                <article className="rounded-lg bg-white p-6 shadow-sm">
                    <div className="flex items-start justify-between gap-4">
                        <div>
                            <p className="text-sm text-gray-500">
                                {data.question.course_title}
                            </p>

                            <h1 className="mt-1 text-2xl font-semibold text-gray-900">
                                {data.question.title}
                            </h1>

                            <p className="mt-2 text-xs text-gray-400">
                                Asked by {data.question.asked_by}
                            </p>
                        </div>

                        <div className="flex items-center gap-2">
                            {data.question.is_resolved && (
                                <span className="rounded-full bg-green-100 px-2.5 py-1 text-xs font-medium text-green-700">
                                    Resolved
                                </span>
                            )}

                            {data.question.is_admin && (
                                <button
                                    type="button"
                                    onClick={
                                        handleModerateQuestion
                                    }
                                    disabled={
                                        isModeratingQuestion
                                    }
                                    className="rounded-md border border-red-300 px-3 py-1.5 text-xs font-medium text-red-700 hover:bg-red-50 disabled:opacity-60"
                                >
                                    {isModeratingQuestion
                                        ? "Updating..."
                                        : "Hide Question"}
                                </button>
                            )}
                        </div>
                    </div>

                    <p className="mt-6 whitespace-pre-wrap text-sm leading-7 text-gray-700">
                        {data.question.body}
                    </p>
                </article>

                {error && (
                    <p
                        className="text-sm text-red-600"
                        role="alert"
                    >
                        {error}
                    </p>
                )}

                <section>
                    <h2 className="mb-3 text-lg font-semibold text-gray-900">
                        {data.answers.length}{" "}
                        {data.answers.length === 1
                            ? "Answer"
                            : "Answers"}
                    </h2>

                    <AnswerList
                        answers={data.answers}
                        currentUserIsQuestionAsker={
                            data.question.is_asker
                        }
                        isAdmin={data.question.is_admin}
                        onVote={handleVote}
                        onAccept={handleAccept}
                        onModerate={handleModerateAnswer}
                        isVoting={isVoting}
                        isAccepting={isAccepting}
                        isModerating={isModeratingAnswer}
                    />
                </section>

                {!data.question.is_asker &&
                    !data.question.is_resolved && (
                        <AnswerForm
                            questionId={data.question.id}
                            onCreated={handleAnswerCreated}
                        />
                    )}
            </div>
        </div>
    );
}