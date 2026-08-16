import api from "./client";

import type {
    ApiResponse,
    Flashcard,
    FlashcardCreateRequest,
    FlashcardDeck,
    FlashcardDeckCreateRequest,
    FlashcardDeckUpdateRequest,
    FlashcardUpdateRequest,
    ProgressUpdateRequest,
    ProgressUpdateResponse,
} from "../types/flashcards";

export async function getDecks(
    courseId?: number,
    query?: string,
): Promise<FlashcardDeck[]> {
    const response = await api.get<ApiResponse<FlashcardDeck[]>>(
        "/flashcards/decks/",
        {
            params: {
                ...(courseId !== undefined && {
                    course_id: courseId,
                }),
                ...(query && {
                    q: query,
                }),
            },
        },
    );

    return response.data.data;
}

export async function createDeck(
    data: FlashcardDeckCreateRequest,
): Promise<FlashcardDeck> {
    const response = await api.post<ApiResponse<FlashcardDeck>>(
        "/flashcards/decks/",
        data,
    );

    return response.data.data;
}

export async function getDeck(
    deckId: number,
): Promise<FlashcardDeck> {
    const response = await api.get<ApiResponse<FlashcardDeck>>(
        `/flashcards/decks/${deckId}/`,
    );

    return response.data.data;
}

export async function updateDeck(
    deckId: number,
    data: FlashcardDeckUpdateRequest,
): Promise<FlashcardDeck> {
    const response = await api.patch<ApiResponse<FlashcardDeck>>(
        `/flashcards/decks/${deckId}/`,
        data,
    );

    return response.data.data;
}

export async function deleteDeck(deckId: number): Promise<void> {
    await api.delete(`/flashcards/decks/${deckId}/`);
}

export async function getCards(
    deckId: number,
): Promise<Flashcard[]> {
    const response = await api.get<ApiResponse<Flashcard[]>>(
        `/flashcards/decks/${deckId}/cards/`,
    );

    return response.data.data;
}

export async function createCard(
    deckId: number,
    data: FlashcardCreateRequest,
): Promise<Flashcard> {
    const response = await api.post<ApiResponse<Flashcard>>(
        `/flashcards/decks/${deckId}/cards/`,
        data,
    );

    return response.data.data;
}

export async function updateCard(
    cardId: number,
    data: FlashcardUpdateRequest,
): Promise<Flashcard> {
    const response = await api.patch<ApiResponse<Flashcard>>(
        `/flashcards/cards/${cardId}/`,
        data,
    );

    return response.data.data;
}

export async function deleteCard(cardId: number): Promise<void> {
    await api.delete(`/flashcards/cards/${cardId}/`);
}

export async function updateCardProgress(
    cardId: number,
    data: ProgressUpdateRequest,
): Promise<ProgressUpdateResponse> {
    const response = await api.post<
        ApiResponse<ProgressUpdateResponse>
    >(
        `/flashcards/cards/${cardId}/progress/`,
        data,
    );

    return response.data.data;
}