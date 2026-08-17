import type {
    QuizQuestion,
} from "../../types/quizzes";

interface Props {
    question: QuizQuestion;
    selectedChoiceId: number | null;
    onSelect: (
        questionId: number,
        choiceId: number | null,
    ) => void;
}

export default function QuizQuestionCard({
    question,
    selectedChoiceId,
    onSelect,
}: Props) {
    return (
        <article className="rounded-lg bg-white p-6 shadow-sm">
            <div className="flex items-start gap-3">
                <span className="shrink-0 font-semibold text-gray-700">
                    {question.order}.
                </span>

                <h2 className="font-medium leading-6 text-gray-900">
                    {question.text}
                </h2>
            </div>

            <div className="mt-5 space-y-2">
                {question.choices.map((choice) => (
                    <label
                        key={choice.id}
                        className={`flex cursor-pointer items-center gap-3 rounded-md border p-3 transition ${
                            selectedChoiceId === choice.id
                                ? "border-blue-500 bg-blue-50"
                                : "border-gray-200 hover:bg-gray-50"
                        }`}
                    >
                        <input
                            type="radio"
                            name={`question-${question.id}`}
                            checked={
                                selectedChoiceId === choice.id
                            }
                            onChange={() =>
                                onSelect(
                                    question.id,
                                    choice.id,
                                )
                            }
                        />

                        <span className="text-sm text-gray-700">
                            {choice.text}
                        </span>
                    </label>
                ))}

                <button
                    type="button"
                    onClick={() =>
                        onSelect(question.id, null)
                    }
                    className={`text-sm ${
                        selectedChoiceId === null
                            ? "text-blue-600"
                            : "text-gray-500"
                    } hover:underline`}
                >
                    Clear selection
                </button>
            </div>
        </article>
    );
}