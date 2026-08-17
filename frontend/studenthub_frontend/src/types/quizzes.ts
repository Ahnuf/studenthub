export interface Quiz {
    id: number;
    course: number;
    course_title: string;
    title: string;
    description: string;
    created_by: string;
    question_count: number;
    is_creator: boolean;
    created_at: string;
    attempts_used: number;
    attempts_remaining: number;
    can_attempt: boolean;
}

export interface QuizQuestionChoice {
    id: number;
    text: string;
}

export interface QuizQuestion {
    id: number;
    text: string;
    order: number;
    choices: QuizQuestionChoice[];
}

export interface QuizQuestionCreatorChoice {
    id: number;
    text: string;
    is_correct: boolean;
    order: number;
}

export interface QuizQuestionCreator {
    id: number;
    text: string;
    order: number;
    choices: QuizQuestionCreatorChoice[];
}

export interface QuizChoiceInput {
    text: string;
    is_correct: boolean;
    order?: number;
}

export interface QuizCreateRequest {
    course: number;
    title: string;
    description?: string;
}

export interface QuizUpdateRequest {
    title?: string;
    description?: string;
}

export interface QuizQuestionCreateRequest {
    text: string;
    order?: number;
    choices: QuizChoiceInput[];
}

export interface QuizQuestionUpdateRequest {
    text?: string;
    order?: number;
    choices?: QuizChoiceInput[];
}

export interface QuizAttemptAnswer {
    question_id: number;
    choice_id: number | null;
}

export interface QuizAttemptSubmitRequest {
    answers: QuizAttemptAnswer[];
}

export interface QuizAttempt {
    id: number;
    total_questions: number;
    correct_answers: number;
    score_percentage: number;
    answers: QuizAttemptAnswerReview[];
    created_at: string;
}

export interface QuizAttemptAnswerReview {
    question_id: number;
    question_text: string;
    choices: QuizChoiceReview[];
    selected_choice_id: number | null;
    is_correct: boolean;
}

export interface QuizChoiceReview {
    id: number;
    text: string;
    is_correct: boolean;
}

export interface ApiResponse<T> {
    success: boolean;
    message: string;
    data: T;
}