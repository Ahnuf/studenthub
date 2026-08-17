import { Link } from "react-router-dom";

import type { QuizAttempt } from "../../types/quizzes";

interface Props {
    attempts: QuizAttempt[];
}

export default function AttemptHistory({
    attempts,
}: Props) {
    if (attempts.length === 0) {
        return (
            <div className="rounded-lg bg-white p-6 shadow-sm">
                <p className="text-sm text-gray-500">
                    You haven't attempted this quiz yet.
                </p>
            </div>
        );
    }

    return (
        <div className="space-y-3">
            {attempts.map((attempt) => (
                <div
                    key={attempt.id}
                    className="flex flex-col gap-3 rounded-lg border border-gray-200 bg-white p-4 sm:flex-row sm:items-center sm:justify-between"
                >
                    <div>
                        <p className="font-medium text-gray-900">
                            {attempt.score_percentage}%
                        </p>

                        <p className="mt-1 text-sm text-gray-500">
                            {attempt.correct_answers} /{" "}
                            {attempt.total_questions} correct
                        </p>

                        <p className="mt-1 text-xs text-gray-400">
                            {new Date(
                                attempt.created_at,
                            ).toLocaleString()}
                        </p>
                    </div>

                    <Link
                        to={`/quizzes/attempts/${attempt.id}`}
                        className="rounded-md border border-gray-300 px-3 py-1.5 text-sm font-medium text-gray-700 hover:bg-gray-50"
                    >
                        Review
                    </Link>
                </div>
            ))}
        </div>
    );
}