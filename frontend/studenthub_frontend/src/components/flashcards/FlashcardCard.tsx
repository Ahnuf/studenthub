import { useState } from "react";

import type {
    Flashcard,
    FlashcardProgressStatus,
} from "../../types/flashcards";

interface Props {
    card: Flashcard;
    onProgressChange: (
        card: Flashcard,
        status: FlashcardProgressStatus,
    ) => void;
    isUpdating: boolean;
}

export default function FlashcardCard({
    card,
    onProgressChange,
    isUpdating,
}: Props) {
    const [showAnswer, setShowAnswer] = useState(false);

    return (
        <article className="rounded-lg bg-white p-6 shadow-sm">
            <div className="min-h-32">
                <p className="whitespace-pre-wrap text-lg text-gray-900">
                    {showAnswer ? card.back : card.front}
                </p>
            </div>

            <div className="mt-6 flex flex-wrap gap-2">
                <button
                    type="button"
                    onClick={() =>
                        setShowAnswer((current) => !current)
                    }
                    className="rounded-md border border-gray-300 px-3 py-1.5 text-sm font-medium text-gray-700 hover:bg-gray-50"
                >
                    {showAnswer ? "Hide Answer" : "Show Answer"}
                </button>

                <button
                    type="button"
                    onClick={() =>
                        onProgressChange(
                            card,
                            "STILL_LEARNING",
                        )
                    }
                    disabled={isUpdating}
                    className={`rounded-md px-3 py-1.5 text-sm font-medium ${
                        card.my_status === "STILL_LEARNING"
                            ? "bg-yellow-100 text-yellow-800"
                            : "border border-gray-300 text-gray-700"
                    } disabled:opacity-60`}
                >
                    Still Learning
                </button>

                <button
                    type="button"
                    onClick={() =>
                        onProgressChange(card, "KNOWN")
                    }
                    disabled={isUpdating}
                    className={`rounded-md px-3 py-1.5 text-sm font-medium ${
                        card.my_status === "KNOWN"
                            ? "bg-green-100 text-green-800"
                            : "border border-gray-300 text-gray-700"
                    } disabled:opacity-60`}
                >
                    Known
                </button>
            </div>
        </article>
    );
}