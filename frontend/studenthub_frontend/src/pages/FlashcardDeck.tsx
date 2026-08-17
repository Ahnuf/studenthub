import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import axios from "axios";

import {
    deleteCard,
    deleteDeck,
    getCards,
    getDeck,
    updateCardProgress,
} from "../api/flashcards";

import CardForm from "../components/flashcards/CardForm";
import DeckForm from "../components/flashcards/DeckForm";
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
    const navigate = useNavigate();

    const [deck, setDeck] = useState<FlashcardDeckType | null>(null);
    const [cards, setCards] = useState<Flashcard[]>([]);
    const [editingCard, setEditingCard] = useState<Flashcard | null>(
        null,
    );

    const [isEditingDeck, setIsEditingDeck] = useState(false);
    const [isDeletingDeck, setIsDeletingDeck] = useState(false);

    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const [updatingCardId, setUpdatingCardId] = useState<number | null>(
        null,
    );
    const [deletingCardId, setDeletingCardId] = useState<number | null>(
        null,
    );

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
                    setError("Failed to load flashcard deck.");
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
            const result = await updateCardProgress(card.id, {
                status,
            });

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
                setError("Failed to update progress.");
            }
        } finally {
            setUpdatingCardId(null);
        }
    }

    function handleCardCreated(card: Flashcard) {
        setCards((current) =>
            [...current, card].sort(
                (a, b) => a.order - b.order || a.id - b.id,
            ),
        );
    }

    function handleCardUpdated(card: Flashcard) {
        setCards((current) =>
            current
                .map((item) => (item.id === card.id ? card : item))
                .sort(
                    (a, b) => a.order - b.order || a.id - b.id,
                ),
        );

        setEditingCard(null);
    }

    async function handleDeleteCard(card: Flashcard) {
        const confirmed = window.confirm(
            "Are you sure you want to delete this flashcard?",
        );

        if (!confirmed) {
            return;
        }

        setDeletingCardId(card.id);
        setError(null);

        try {
            await deleteCard(card.id);

            setCards((current) =>
                current.filter((item) => item.id !== card.id),
            );

            if (editingCard?.id === card.id) {
                setEditingCard(null);
            }
        } catch (err: unknown) {
            if (axios.isAxiosError<ApiErrorResponse>(err)) {
                setError(
                    err.response?.data?.message ??
                        "Failed to delete flashcard.",
                );
            } else {
                setError("Failed to delete flashcard.");
            }
        } finally {
            setDeletingCardId(null);
        }
    }

    function handleDeckUpdated(updatedDeck: FlashcardDeckType) {
        setDeck(updatedDeck);
        setIsEditingDeck(false);
    }

    async function handleDeleteDeck() {
        if (!deck) {
            return;
        }

        const confirmed = window.confirm(
            `Are you sure you want to delete "${deck.title}"? This will also remove its flashcards.`,
        );

        if (!confirmed) {
            return;
        }

        setIsDeletingDeck(true);
        setError(null);

        try {
            await deleteDeck(deck.id);
            navigate("/flashcards");
        } catch (err: unknown) {
            if (axios.isAxiosError<ApiErrorResponse>(err)) {
                setError(
                    err.response?.data?.message ??
                        "Failed to delete deck.",
                );
            } else {
                setError("Failed to delete deck.");
            }

            setIsDeletingDeck(false);
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
                    <p className="text-sm text-red-600">{error}</p>

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

    if (isEditingDeck) {
        return (
            <div className="p-6">
                <div className="mx-auto max-w-4xl space-y-6">
                    <Link
                        to={`/flashcards/decks/${deck.id}`}
                        className="text-sm text-blue-600 hover:underline"
                    >
                        ← Back to Deck
                    </Link>

                    <DeckForm
                        editingDeck={deck}
                        onCreated={() => undefined}
                        onUpdated={handleDeckUpdated}
                        onCancelEdit={() =>
                            setIsEditingDeck(false)
                        }
                    />
                </div>
            </div>
        );
    }

    const knownCount = cards.filter(
        (card) => card.my_status === "KNOWN",
    ).length;

    const nextOrder =
        cards.length > 0
            ? Math.max(...cards.map((card) => card.order)) + 1
            : 0;

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
                    <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
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

                            <p className="mt-3 text-xs text-gray-400">
                                Created by {deck.created_by}
                            </p>
                        </div>

                        <div className="flex flex-col items-end gap-3">
                            <div className="rounded-lg bg-gray-50 px-4 py-3 text-sm text-gray-600">
                                <p>
                                    {knownCount} / {cards.length} known
                                </p>
                            </div>

                            {deck.is_creator && (
                                <div className="flex gap-2">
                                    <button
                                        type="button"
                                        onClick={() =>
                                            setIsEditingDeck(true)
                                        }
                                        className="rounded-md border border-gray-300 px-3 py-1.5 text-sm font-medium text-gray-700 hover:bg-gray-50"
                                    >
                                        Edit Deck
                                    </button>

                                    <button
                                        type="button"
                                        onClick={() =>
                                            void handleDeleteDeck()
                                        }
                                        disabled={isDeletingDeck}
                                        className="rounded-md bg-red-600 px-3 py-1.5 text-sm font-medium text-white hover:bg-red-700 disabled:opacity-60"
                                    >
                                        {isDeletingDeck
                                            ? "Deleting..."
                                            : "Delete Deck"}
                                    </button>
                                </div>
                            )}
                        </div>
                    </div>
                </section>

                {deck.is_creator && (
                    <CardForm
                        deckId={deck.id}
                        editingCard={editingCard}
                        nextOrder={nextOrder}
                        onCreated={handleCardCreated}
                        onUpdated={handleCardUpdated}
                        onCancelEdit={() => setEditingCard(null)}
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

                {cards.length === 0 ? (
                    <div className="rounded-lg bg-white p-6 shadow-sm">
                        <p className="text-sm text-gray-500">
                            This deck has no flashcards yet.
                        </p>
                    </div>
                ) : (
                    <div className="space-y-4">
                        {cards.map((card) => (
                            <div
                                key={card.id}
                                className="space-y-2"
                            >
                                <FlashcardCard
                                    card={card}
                                    onProgressChange={
                                        handleProgressChange
                                    }
                                    isUpdating={
                                        updatingCardId === card.id
                                    }
                                />

                                {deck.is_creator && (
                                    <div className="flex justify-end gap-2">
                                        <button
                                            type="button"
                                            onClick={() =>
                                                setEditingCard(card)
                                            }
                                            className="rounded-md border border-gray-300 px-3 py-1.5 text-sm text-gray-700 hover:bg-gray-50"
                                        >
                                            Edit
                                        </button>

                                        <button
                                            type="button"
                                            onClick={() =>
                                                void handleDeleteCard(
                                                    card,
                                                )
                                            }
                                            disabled={
                                                deletingCardId === card.id
                                            }
                                            className="rounded-md bg-red-600 px-3 py-1.5 text-sm text-white hover:bg-red-700 disabled:opacity-60"
                                        >
                                            {deletingCardId === card.id
                                                ? "Deleting..."
                                                : "Delete"}
                                        </button>
                                    </div>
                                )}
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
}