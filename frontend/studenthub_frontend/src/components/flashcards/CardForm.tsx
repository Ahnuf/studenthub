"use no memo";

import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import axios from "axios";

import {
    createCard,
    updateCard,
} from "../../api/flashcards";

import type {
    Flashcard,
    FlashcardCreateRequest,
    FlashcardUpdateRequest,
} from "../../types/flashcards";

interface Props {
    deckId: number;
    editingCard?: Flashcard | null;
    nextOrder: number;
    onCreated: (card: Flashcard) => void;
    onUpdated: (card: Flashcard) => void;
    onCancelEdit: () => void;
}

interface CardFormData {
    front: string;
    back: string;
    order: number;
}

interface ApiErrorResponse {
    success: boolean;
    message: string;
}

export default function CardForm({
    deckId,
    editingCard,
    nextOrder,
    onCreated,
    onUpdated,
    onCancelEdit,
}: Props) {
    const [serverError, setServerError] = useState<string | null>(
        null,
    );
    const [isSubmitting, setIsSubmitting] = useState(false);

    const {
        register,
        handleSubmit,
        reset,
        formState: { errors },
    } = useForm<CardFormData>({
        defaultValues: {
            front: editingCard?.front ?? "",
            back: editingCard?.back ?? "",
            order: editingCard?.order ?? nextOrder,
        },
    });

    useEffect(() => {
        reset({
            front: editingCard?.front ?? "",
            back: editingCard?.back ?? "",
            order: editingCard?.order ?? nextOrder,
        });
    }, [editingCard, nextOrder, reset]);

    async function onSubmit(data: CardFormData) {
        setServerError(null);
        setIsSubmitting(true);

        try {
            if (editingCard) {
                const payload: FlashcardUpdateRequest = {
                    front: data.front,
                    back: data.back,
                    order: data.order,
                };

                const updatedCard = await updateCard(
                    editingCard.id,
                    payload,
                );

                onUpdated(updatedCard);
            } else {
                const payload: FlashcardCreateRequest = {
                    front: data.front,
                    back: data.back,
                    order: data.order,
                };

                const createdCard = await createCard(
                    deckId,
                    payload,
                );

                onCreated(createdCard);

                reset({
                    front: "",
                    back: "",
                    order: nextOrder + 1,
                });
            }
        } catch (err: unknown) {
            if (axios.isAxiosError<ApiErrorResponse>(err)) {
                setServerError(
                    err.response?.data?.message ??
                        "Failed to save flashcard.",
                );
            } else {
                setServerError(
                    "Failed to save flashcard.",
                );
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
                {editingCard
                    ? "Edit Flashcard"
                    : "Add Flashcard"}
            </h2>

            <div>
                <label className="mb-1 block text-sm font-medium text-gray-700">
                    Front
                </label>

                <textarea
                    rows={4}
                    placeholder="Question or prompt"
                    {...register("front", {
                        required: "Front is required",
                    })}
                    className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                />

                {errors.front && (
                    <p className="mt-1 text-sm text-red-600">
                        {errors.front.message}
                    </p>
                )}
            </div>

            <div>
                <label className="mb-1 block text-sm font-medium text-gray-700">
                    Back
                </label>

                <textarea
                    rows={4}
                    placeholder="Answer or explanation"
                    {...register("back", {
                        required: "Back is required",
                    })}
                    className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                />

                {errors.back && (
                    <p className="mt-1 text-sm text-red-600">
                        {errors.back.message}
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
                        : editingCard
                          ? "Save Changes"
                          : "Add Card"}
                </button>

                {editingCard && (
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