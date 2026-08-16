import { Link } from "react-router-dom";

import type { FlashcardDeck } from "../../types/flashcards";

interface Props {
    decks: FlashcardDeck[];
}

export default function DeckList({ decks }: Props) {
    if (decks.length === 0) {
        return (
            <div className="rounded-lg bg-white p-6 shadow-sm">
                <p className="text-sm text-gray-500">
                    No flashcard decks found.
                </p>
            </div>
        );
    }

    return (
        <div className="grid gap-4 md:grid-cols-2">
            {decks.map((deck) => (
                <Link
                    key={deck.id}
                    to={`/flashcards/decks/${deck.id}`}
                    className="block rounded-lg border border-gray-200 bg-white p-5 transition hover:border-blue-300 hover:bg-blue-50"
                >
                    <div className="flex items-start justify-between gap-4">
                        <div className="min-w-0">
                            <h2 className="font-semibold text-gray-900">
                                {deck.title}
                            </h2>

                            <p className="mt-1 text-sm text-gray-500">
                                {deck.course_title}
                            </p>

                            {deck.description && (
                                <p className="mt-2 line-clamp-2 text-sm text-gray-600">
                                    {deck.description}
                                </p>
                            )}

                            <p className="mt-3 text-xs text-gray-400">
                                Created by {deck.created_by}
                            </p>
                        </div>

                        <span className="shrink-0 rounded-full bg-gray-100 px-2.5 py-1 text-xs font-medium text-gray-600">
                            {deck.card_count}{" "}
                            {deck.card_count === 1
                                ? "card"
                                : "cards"}
                        </span>
                    </div>
                </Link>
            ))}
        </div>
    );
}