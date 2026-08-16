import { useState } from "react";
import axios from "axios";
import { useForm } from "react-hook-form";

import { createAnswer } from "../../api/qa";

import type { Answer } from "../../types/qa";

interface Props {
    questionId: number;
    onCreated: (answer: Answer) => void;
}

interface AnswerFormData {
    body: string;
}

interface ApiErrorResponse {
    success: boolean;
    message: string;
}

export default function AnswerForm({
    questionId,
    onCreated,
}: Props) {
    const [serverError, setServerError] = useState<string | null>(null);
    const [isSubmitting, setIsSubmitting] = useState(false);

    const {
        register,
        handleSubmit,
        reset,
        formState: { errors },
    } = useForm<AnswerFormData>();

    async function onSubmit(data: AnswerFormData) {
        setServerError(null);
        setIsSubmitting(true);

        try {
            const answer = await createAnswer(questionId, data);

            onCreated(answer);
            reset();
        } catch (err: unknown) {
            if (axios.isAxiosError<ApiErrorResponse>(err)) {
                setServerError(
                    err.response?.data?.message ??
                        "Failed to post answer.",
                );
            } else {
                setServerError("Failed to post answer.");
            }
        } finally {
            setIsSubmitting(false);
        }
    }

    return (
        <form
            onSubmit={handleSubmit(onSubmit)}
            className="space-y-4 rounded-lg bg-white p-6 shadow-sm"
        >
            <h2 className="font-semibold text-gray-900">
                Your Answer
            </h2>

            <textarea
                rows={6}
                placeholder="Write your answer..."
                {...register("body", {
                    required: "Answer cannot be empty",
                })}
                className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
            />

            {errors.body && (
                <p className="text-sm text-red-600">
                    {errors.body.message}
                </p>
            )}

            {serverError && (
                <p
                    className="text-sm text-red-600"
                    role="alert"
                >
                    {serverError}
                </p>
            )}

            <button
                type="submit"
                disabled={isSubmitting}
                className="rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-60"
            >
                {isSubmitting ? "Posting..." : "Post Answer"}
            </button>
        </form>
    );
}