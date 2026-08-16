export interface Question {
    id: number;
    course: number;
    course_title: string;
    title: string;
    asked_by: string;
    answer_count: number;
    is_resolved: boolean;
    is_asker: boolean;
    is_admin: boolean;
    created_at: string;
}

export interface QuestionDetail extends Question {
    body: string;
}

export interface Answer {
    id: number;
    body: string;
    answered_by: string;
    is_accepted: boolean;
    vote_count: number;
    has_voted: boolean;
    is_admin: boolean;
    created_at: string;
}

export interface QuestionCreateRequest {
    course: number;
    title: string;
    body: string;
}

export interface AnswerCreateRequest {
    body: string;
}

export interface VoteResult {
    has_voted: boolean;
    vote_count: number;
}

export interface QuestionDetailData {
    question: QuestionDetail;
    answers: Answer[];
}

export interface ApiResponse<T> {
    success: boolean;
    message: string;
    data: T;
}

export interface ModerationRequest {
    is_active: boolean;
}