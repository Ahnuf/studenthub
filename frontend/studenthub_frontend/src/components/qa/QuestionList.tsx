import { Link } from "react-router-dom";

import type { Question } from "../../types/qa";

interface Props {
    questions: Question[];
}

export default function QuestionList({ questions }: Props) {
    if (questions.length === 0) {
        return (
            <div className="rounded-lg bg-white p-6 shadow-sm">
                <p className="text-sm text-gray-500">
                    No questions found.
                </p>
            </div>
        );
    }

    return (
        <div className="space-y-3">
            {questions.map((question) => (
                <Link
                    key={question.id}
                    to={`/qa/questions/${question.id}`}
                    className="block rounded-lg border border-gray-200 bg-white p-4 transition hover:border-blue-300 hover:bg-blue-50"
                >
                    <div className="flex items-start justify-between gap-4">
                        <div className="min-w-0">
                            <h3 className="font-medium text-gray-900">
                                {question.title}
                            </h3>

                            <p className="mt-1 text-sm text-gray-500">
                                {question.course_title}
                            </p>

                            <p className="mt-1 text-xs text-gray-400">
                                Asked by {question.asked_by}
                            </p>
                        </div>

                        <div className="shrink-0 text-right text-xs text-gray-500">
                            <p>
                                {question.answer_count}{" "}
                                {question.answer_count === 1
                                    ? "answer"
                                    : "answers"}
                            </p>

                            <p className="mt-1">
                                {question.is_resolved
                                    ? "Resolved"
                                    : "Open"}
                            </p>
                        </div>
                    </div>
                </Link>
            ))}
        </div>
    );
}