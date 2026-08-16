export type FlashcardProgressStatus =
    | "STILL_LEARNING"
    | "KNOWN";

export interface FlashcardDeck {
    id: number;
    course: number;
    course_title: string;
    title: string;
    description: string;
    created_by: string;
    card_count: number;
    created_at: string;
    updated_at: string;
}

export interface Flashcard {
    id: number;
    front: string;
    back: string;
    order: number;
    my_status: FlashcardProgressStatus;
    created_at: string;
    updated_at: string;
}

export interface FlashcardDeckCreateRequest {
    course: number;
    title: string;
    description?: string;
}

export interface FlashcardDeckUpdateRequest {
    title?: string;
    description?: string;
}

export interface FlashcardCreateRequest {
    front: string;
    back: string;
    order?: number;
}

export interface FlashcardUpdateRequest {
    front?: string;
    back?: string;
    order?: number;
}

export interface ProgressUpdateRequest {
    status: FlashcardProgressStatus;
}

export interface ProgressUpdateResponse {
    card_id: number;
    status: FlashcardProgressStatus;
}

export interface ApiResponse<T> {
    success: boolean;
    message: string;
    data: T;
}