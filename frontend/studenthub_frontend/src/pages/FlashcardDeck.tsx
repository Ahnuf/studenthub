import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import axios from "axios";

import {
    getCards,
    getDeck,
    updateCardProgress,
} from "../api/flashcards";

import FlashcardCard from "../components/flashcards/FlashcardCard";

import type {
    Flashcard,
    FlashcardDeck as FlashcardDeckType,
    FlashcardProgressStatus,
} from "../types/flashcards";

interface ApiErrorResponse {
    success: boolean;
    message: string;
}

export default function FlashcardDeck() {
    const { deckId } = useParams();

    const [deck, setDeck] = useState<FlashcardDeckType | null>(
        null,
    );
    const [cards, setCards] = useState<Flashcard[]>([]);

    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [updatingCardId, setUpdatingCardId] = useState<
        number | null
    >(null);

    useEffect(() => {
        if (!deckId) {
            return;
        }

        async function loadDeck() {
            try {
                const id = Number(deckId);

                const [deckData, cardsData] = await Promise.all([
                    getDeck(id),
                    getCards(id),
                ]);

                setDeck(deckData);
                setCards(cardsData);
            } catch (err: unknown) {
                if (axios.isAxiosError<ApiErrorResponse>(err)) {
                    setError(
                        err.response?.data?.message ??
                            "Failed to load flashcard deck.",
                    );
                } else {
                    setError(
                        "Failed to load flashcard deck.",
                    );
                }
            } finally {
                setIsLoading(false);
            }
        }

        loadDeck();
    }, [deckId]);

    async function handleProgressChange(
        card: Flashcard,
        status: FlashcardProgressStatus,
    ) {
        setUpdatingCardId(card.id);
        setError(null);

        try {
            const result = await updateCardProgress(
                card.id,
                { status },
            );

            setCards((current) =>
                current.map((item) =>
                    item.id === card.id
                        ? {
                              ...item,
                              my_status: result.status,
                          }
                        : item,
                ),
            );
        } catch (err: unknown) {
            if (axios.isAxiosError<ApiErrorResponse>(err)) {
                setError(
                    err.response?.data?.message ??
                        "Failed to update progress.",
                );
            } else {
                setError(
                    "Failed to update progress.",
                );
            }
        } finally {
            setUpdatingCardId(null);
        }
    }

    if (!deckId) {
        return (
            <div className="p-6">
                <div className="mx-auto max-w-4xl">
                    <p className="text-sm text-red-600">
                        Deck not found.
                    </p>

                    <Link
                        to="/flashcards"
                        className="mt-4 inline-block text-sm text-blue-600 hover:underline"
                    >
                        Back to Flashcards
                    </Link>
                </div>
            </div>
        );
    }

    if (isLoading) {
        return (
            <div className="flex items-center justify-center py-24">
                <p className="text-gray-500">
                    Loading flashcards...
                </p>
            </div>
        );
    }

    if (error && !deck) {
        return (
            <div className="p-6">
                <div className="mx-auto max-w-4xl">
                    <p className="text-sm text-red-600">
                        {error}
                    </p>

                    <Link
                        to="/flashcards"
                        className="mt-4 inline-block text-sm text-blue-600 hover:underline"
                    >
                        Back to Flashcards
                    </Link>
                </div>
            </div>
        );
    }

    if (!deck) {
        return null;
    }

    const knownCount = cards.filter(
        (card) => card.my_status === "KNOWN",
    ).length;

    return (
        <div className="p-6">
            <div className="mx-auto max-w-4xl space-y-6">
                <Link
                    to="/flashcards"
                    className="text-sm text-blue-600 hover:underline"
                >
                    ← Back to Flashcards
                </Link>

                <section className="rounded-lg bg-white p-6 shadow-sm">
                    <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
                        <div>
                            <p className="text-sm text-gray-500">
                                {deck.course_title}
                            </p>

                            <h1 className="mt-1 text-2xl font-semibold text-gray-900">
                                {deck.title}
                            </h1>

                            {deck.description && (
                                <p className="mt-2 text-sm leading-6 text-gray-600">
                                    {deck.description}
                                </p>
                            )}
                        </div>

                        <div className="shrink-0 rounded-lg bg-gray-50 px-4 py-3 text-sm text-gray-600">
                            <p>
                                {knownCount} / {cards.length} known
                            </p>
                        </div>
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

                {cards.length === 0 ? (
                    <div className="rounded-lg bg-white p-6 shadow-sm">
                        <p className="text-sm text-gray-500">
                            This deck has no flashcards yet.
                        </p>
                    </div>
                ) : (
                    <div className="space-y-4">
                        {cards.map((card) => (
                            <FlashcardCard
                                key={card.id}
                                card={card}
                                onProgressChange={
                                    handleProgressChange
                                }
                                isUpdating={
                                    updatingCardId === card.id
                                }
                            />
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
}