/* eslint-disable react-hooks/set-state-in-effect */
"use no memo";

import { useEffect, useState } from "react";
import axios from "axios";
import { useForm } from "react-hook-form";

import {
    createQuizQuestion,
    updateQuizQuestion,
} from "../../api/quizzes";

import type {
    QuizChoiceInput,
    QuizQuestion,
    QuizQuestionCreateRequest,
    QuizQuestionUpdateRequest,
} from "../../types/quizzes";

interface Props {
    quizId: number;
    editingQuestion?: QuizQuestion | null;
    nextOrder: number;
    onCreated: (question: QuizQuestion) => void;
    onUpdated: (question: QuizQuestion) => void;
    onCancelEdit: () => void;
}

interface QuestionFormData {
    text: string;
    order: number;
}

interface ChoiceRow {
    id: number;
    text: string;
    is_correct: boolean;
}

interface ApiErrorResponse {
    success: boolean;
    message: string;
}

function createEmptyChoices(): ChoiceRow[] {
    return [
        { id: 1, text: "", is_correct: true },
        { id: 2, text: "", is_correct: false },
    ];
}

export default function QuizQuestionForm({
    quizId,
    editingQuestion,
    nextOrder,
    onCreated,
    onUpdated,
    onCancelEdit,
}: Props) {
    const [choices, setChoices] = useState<ChoiceRow[]>(
        createEmptyChoices(),
    );

    const [serverError, setServerError] = useState<string | null>(
        null,
    );

    const [isSubmitting, setIsSubmitting] = useState(false);

    const {
        register,
        handleSubmit,
        reset,
        formState: { errors },
    } = useForm<QuestionFormData>({
        defaultValues: {
            text: editingQuestion?.text ?? "",
            order: editingQuestion?.order ?? nextOrder,
        },
    });

    useEffect(() => {
        reset({
            text: editingQuestion?.text ?? "",
            order: editingQuestion?.order ?? nextOrder,
        });

        setServerError(null);

        if (editingQuestion) {
            setChoices(
                editingQuestion.choices.map((choice) => ({
                    id: choice.id,
                    text: choice.text,
                    is_correct: false,
                })),
            );
        } else {
            setChoices(createEmptyChoices());
        }
    }, [editingQuestion, nextOrder, reset]);

    function updateChoice(
        index: number,
        field: "text" | "is_correct",
        value: string | boolean,
    ) {
        setChoices((current) =>
            current.map((choice, choiceIndex) => {
                if (field === "is_correct" && value === true) {
                    return {
                        ...choice,
                        is_correct: choiceIndex === index,
                    };
                }

                if (choiceIndex === index) {
                    return {
                        ...choice,
                        [field]: value,
                    };
                }

                return choice;
            }),
        );
    }

    function addChoice() {
        const nextId =
            Math.max(
                0,
                ...choices.map((choice) => choice.id),
            ) + 1;

        setChoices((current) => [
            ...current,
            {
                id: nextId,
                text: "",
                is_correct: false,
            },
        ]);
    }

    function removeChoice(index: number) {
        if (choices.length <= 2) {
            return;
        }

        setChoices((current) =>
            current.filter(
                (_, choiceIndex) => choiceIndex !== index,
            ),
        );
    }

    async function onSubmit(data: QuestionFormData) {
        setServerError(null);

        if (choices.length < 2) {
            setServerError(
                "A question needs at least 2 choices.",
            );
            return;
        }

        const correctCount = choices.filter(
            (choice) => choice.is_correct,
        ).length;

        if (correctCount !== 1) {
            setServerError(
                "Exactly one choice must be marked correct.",
            );
            return;
        }

        const emptyChoice = choices.some(
            (choice) => choice.text.trim() === "",
        );

        if (emptyChoice) {
            setServerError(
                "Every choice must have text.",
            );
            return;
        }

        setIsSubmitting(true);

        try {
            const preparedChoices: QuizChoiceInput[] =
                choices.map((choice, index) => ({
                    text: choice.text.trim(),
                    is_correct: choice.is_correct,
                    order: index,
                }));

            if (editingQuestion) {
                const payload: QuizQuestionUpdateRequest = {
                    text: data.text,
                    order: data.order,
                    choices: preparedChoices,
                };

                const updatedQuestion =
                    await updateQuizQuestion(
                        editingQuestion.id,
                        payload,
                    );

                onUpdated(updatedQuestion);
            } else {
                const payload: QuizQuestionCreateRequest = {
                    text: data.text,
                    order: data.order,
                    choices: preparedChoices,
                };

                const createdQuestion =
                    await createQuizQuestion(
                        quizId,
                        payload,
                    );

                onCreated(createdQuestion);

                reset({
                    text: "",
                    order: nextOrder + 1,
                });

                setChoices(createEmptyChoices());
            }
        } catch (err: unknown) {
            if (axios.isAxiosError<ApiErrorResponse>(err)) {
                setServerError(
                    err.response?.data?.message ??
                        "Failed to save question.",
                );
            } else {
                setServerError(
                    "Failed to save question.",
                );
            }
        } finally {
            setIsSubmitting(false);
        }
    }

    return (
        <form
            onSubmit={handleSubmit(onSubmit)}
            className="space-y-5 rounded-lg bg-white p-6 shadow-sm"
        >
            <h2 className="font-semibold text-gray-900">
                {editingQuestion
                    ? "Edit Question"
                    : "Add Question"}
            </h2>

            <div>
                <label className="mb-1 block text-sm font-medium text-gray-700">
                    Question
                </label>

                <textarea
                    rows={4}
                    placeholder="Enter the question..."
                    {...register("text", {
                        required: "Question text is required",
                    })}
                    className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                />

                {errors.text && (
                    <p className="mt-1 text-sm text-red-600">
                        {errors.text.message}
                    </p>
                )}
            </div>

            <div>
                <label className="mb-1 block text-sm font-medium text-gray-700">
                    Order
                </label>

                <input
                    type="number"
                    min={0}
                    {...register("order", {
                        required: "Order is required",
                        valueAsNumber: true,
                        min: {
                            value: 0,
                            message: "Order cannot be negative",
                        },
                    })}
                    className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm"
                />

                {errors.order && (
                    <p className="mt-1 text-sm text-red-600">
                        {errors.order.message}
                    </p>
                )}
            </div>

            <div className="space-y-3">
                <div className="flex items-center justify-between">
                    <div>
                        <h3 className="font-medium text-gray-900">
                            Choices
                        </h3>

                        <p className="text-xs text-gray-500">
                            Exactly one choice must be correct.
                        </p>
                    </div>

                    <button
                        type="button"
                        onClick={addChoice}
                        className="rounded-md border border-gray-300 px-3 py-1.5 text-sm text-gray-700 hover:bg-gray-50"
                    >
                        Add Choice
                    </button>
                </div>

                {choices.map((choice, index) => (
                    <div
                        key={choice.id}
                        className="rounded-md border border-gray-200 p-3"
                    >
                        <div className="flex gap-2">
                            <input
                                type="text"
                                value={choice.text}
                                onChange={(event) =>
                                    updateChoice(
                                        index,
                                        "text",
                                        event.target.value,
                                    )
                                }
                                placeholder={`Choice ${
                                    index + 1
                                }`}
                                className="flex-1 rounded-md border border-gray-300 px-3 py-2 text-sm"
                            />

                            <button
                                type="button"
                                onClick={() =>
                                    removeChoice(index)
                                }
                                disabled={choices.length <= 2}
                                className="rounded-md border border-red-300 px-3 py-2 text-sm text-red-700 hover:bg-red-50 disabled:cursor-not-allowed disabled:opacity-40"
                            >
                                Remove
                            </button>
                        </div>

                        <label className="mt-2 flex items-center gap-2 text-sm text-gray-600">
                            <input
                                type="radio"
                                name="correct-choice"
                                checked={choice.is_correct}
                                onChange={() =>
                                    updateChoice(
                                        index,
                                        "is_correct",
                                        true,
                                    )
                                }
                            />

                            Correct answer
                        </label>
                    </div>
                ))}
            </div>

            {serverError && (
                <p
                    className="text-sm text-red-600"
                    role="alert"
                >
                    {serverError}
                </p>
            )}

            <div className="flex gap-3">
                <button
                    type="submit"
                    disabled={isSubmitting}
                    className="rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-60"
                >
                    {isSubmitting
                        ? "Saving..."
                        : editingQuestion
                          ? "Save Changes"
                          : "Add Question"}
                </button>

                {editingQuestion && (
                    <button
                        type="button"
                        onClick={onCancelEdit}
                        disabled={isSubmitting}
                        className="rounded-md border border-gray-300 px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 disabled:opacity-60"
                    >
                        Cancel
                    </button>
                )}
            </div>
        </form>
    );
}