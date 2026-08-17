import api from "./client";

import type {
    ApiResponse,
    Quiz,
    QuizAttempt,
    QuizCreateRequest,
    QuizQuestion,
    QuizQuestionCreator,
    QuizQuestionCreateRequest,
    QuizQuestionUpdateRequest,
    QuizAttemptSubmitRequest,
    QuizUpdateRequest,
} from "../types/quizzes";

export async function getQuizzes(
    courseId?: number,
    query?: string,
): Promise<Quiz[]> {
    const response = await api.get<ApiResponse<Quiz[]>>(
        "/quizzes/",
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

export async function createQuiz(
    data: QuizCreateRequest,
): Promise<Quiz> {
    const response = await api.post<ApiResponse<Quiz>>(
        "/quizzes/",
        data,
    );

    return response.data.data;
}

export async function getQuiz(
    quizId: number,
): Promise<Quiz> {
    const response = await api.get<ApiResponse<Quiz>>(
        `/quizzes/${quizId}/`,
    );

    return response.data.data;
}

export async function updateQuiz(
    quizId: number,
    data: QuizUpdateRequest,
): Promise<Quiz> {
    const response = await api.patch<ApiResponse<Quiz>>(
        `/quizzes/${quizId}/`,
        data,
    );

    return response.data.data;
}

export async function deleteQuiz(
    quizId: number,
): Promise<void> {
    await api.delete(`/quizzes/${quizId}/`);
}

export async function getQuizQuestions(
    quizId: number,
): Promise<QuizQuestion[]> {
    const response = await api.get<
        ApiResponse<QuizQuestion[]>
    >(
        `/quizzes/${quizId}/questions/`,
    );

    return response.data.data;
}

export async function createQuizQuestion(
    quizId: number,
    data: QuizQuestionCreateRequest,
): Promise<QuizQuestion> {
    const response = await api.post<
        ApiResponse<QuizQuestion>
    >(
        `/quizzes/${quizId}/questions/`,
        data,
    );

    return response.data.data;
}

export async function updateQuizQuestion(
    questionId: number,
    data: QuizQuestionUpdateRequest,
): Promise<QuizQuestion> {
    const response = await api.patch<
        ApiResponse<QuizQuestion>
    >(
        `/quizzes/questions/${questionId}/`,
        data,
    );

    return response.data.data;
}

export async function deleteQuizQuestion(
    questionId: number,
): Promise<void> {
    await api.delete(
        `/quizzes/questions/${questionId}/`,
    );
}

export async function getQuizAttempts(
    quizId: number,
): Promise<QuizAttempt[]> {
    const response = await api.get<
        ApiResponse<QuizAttempt[]>
    >(
        `/quizzes/${quizId}/attempts/`,
    );

    return response.data.data;
}

export async function submitQuizAttempt(
    quizId: number,
    data: QuizAttemptSubmitRequest,
): Promise<QuizAttempt> {
    const response = await api.post<
        ApiResponse<QuizAttempt>
    >(
        `/quizzes/${quizId}/attempts/`,
        data,
    );

    return response.data.data;
}

export async function getQuizAttempt(
    attemptId: number,
): Promise<QuizAttempt> {
    const response = await api.get<
        ApiResponse<QuizAttempt>
    >(
        `/quizzes/attempts/${attemptId}/`,
    );

    return response.data.data;
}

export async function getQuizQuestionForCreator(
    questionId: number,
): Promise<QuizQuestionCreator> {
    const response = await api.get<
        ApiResponse<QuizQuestionCreator>
    >(
        `/quizzes/questions/${questionId}/`,
    );

    return response.data.data;
}