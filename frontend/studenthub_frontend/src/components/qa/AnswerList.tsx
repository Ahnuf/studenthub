import type { Answer } from "../../types/qa";

interface Props {
    answers: Answer[];
    currentUserIsQuestionAsker: boolean;
    isAdmin: boolean;
    onVote: (answer: Answer) => void;
    onAccept: (answer: Answer) => void;
    onModerate: (answer: Answer) => void;
    isVoting: number | null;
    isAccepting: number | null;
    isModerating: number | null;
}

export default function AnswerList({
    answers,
    currentUserIsQuestionAsker,
    isAdmin,
    onVote,
    onAccept,
    onModerate,
    isVoting,
    isAccepting,
    isModerating,
}: Props) {
    if (answers.length === 0) {
        return (
            <div className="rounded-lg bg-white p-6 shadow-sm">
                <p className="text-sm text-gray-500">
                    No answers yet. Be the first to answer.
                </p>
            </div>
        );
    }

    return (
        <div className="space-y-3">
            {answers.map((answer) => (
                <article
                    key={answer.id}
                    className={`rounded-lg border bg-white p-5 shadow-sm ${
                        answer.is_accepted
                            ? "border-green-300"
                            : "border-gray-200"
                    }`}
                >
                    <div className="flex items-start justify-between gap-4">
                        <div className="min-w-0 flex-1">
                            <p className="whitespace-pre-wrap text-sm leading-6 text-gray-700">
                                {answer.body}
                            </p>

                            <p className="mt-3 text-xs text-gray-400">
                                Answered by {answer.answered_by}
                            </p>
                        </div>

                        <div className="flex shrink-0 items-center gap-2">
                            {answer.is_accepted && (
                                <span className="rounded-full bg-green-100 px-2.5 py-1 text-xs font-medium text-green-700">
                                    Accepted
                                </span>
                            )}

                            {isAdmin && (
                                <button
                                    type="button"
                                    onClick={() =>
                                        onModerate(answer)
                                    }
                                    disabled={
                                        isModerating === answer.id
                                    }
                                    className="rounded-md border border-red-300 px-2.5 py-1 text-xs font-medium text-red-700 hover:bg-red-50 disabled:opacity-60"
                                >
                                    {isModerating === answer.id
                                        ? "Updating..."
                                        : "Hide Answer"}
                                </button>
                            )}
                        </div>
                    </div>

                    <div className="mt-4 flex items-center gap-3">
                        <button
                            type="button"
                            onClick={() => onVote(answer)}
                            disabled={isVoting === answer.id}
                            className={`rounded-md border px-3 py-1.5 text-sm ${
                                answer.has_voted
                                    ? "border-blue-300 bg-blue-50 text-blue-700"
                                    : "border-gray-300 text-gray-700"
                            } disabled:opacity-60`}
                        >
                            {answer.has_voted
                                ? "▲ Upvoted"
                                : "▲ Upvote"}{" "}
                            ({answer.vote_count})
                        </button>

                        {currentUserIsQuestionAsker &&
                            !answer.is_accepted && (
                                <button
                                    type="button"
                                    onClick={() => onAccept(answer)}
                                    disabled={
                                        isAccepting === answer.id
                                    }
                                    className="rounded-md border border-gray-300 px-3 py-1.5 text-sm text-gray-700 hover:bg-gray-50 disabled:opacity-60"
                                >
                                    {isAccepting === answer.id
                                        ? "Accepting..."
                                        : "Accept answer"}
                                </button>
                            )}
                    </div>
                </article>
            ))}
        </div>
    );
}