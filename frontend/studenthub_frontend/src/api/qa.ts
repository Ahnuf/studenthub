import api from "./client";

import type {
    Answer,
    AnswerCreateRequest,
    ApiResponse,
    ModerationRequest,
    Question,
    QuestionCreateRequest,
    QuestionDetail,
    QuestionDetailData,
    VoteResult,
} from "../types/qa";

export async function getQuestions(
    courseId?: number,
): Promise<Question[]> {
    const response = await api.get<ApiResponse<Question[]>>(
        "/qa/questions/",
        {
            params: {
                ...(courseId !== undefined && {
                    course_id: courseId,
                }),
            },
        },
    );

    return response.data.data;
}

export async function createQuestion(
    data: QuestionCreateRequest,
): Promise<QuestionDetail> {
    const response = await api.post<ApiResponse<QuestionDetail>>(
        "/qa/questions/",
        data,
    );

    return response.data.data;
}

export async function getQuestion(
    questionId: number,
): Promise<QuestionDetailData> {
    const response = await api.get<ApiResponse<QuestionDetailData>>(
        `/qa/questions/${questionId}/`,
    );

    return response.data.data;
}

export async function createAnswer(
    questionId: number,
    data: AnswerCreateRequest,
): Promise<Answer> {
    const response = await api.post<ApiResponse<Answer>>(
        `/qa/questions/${questionId}/answers/`,
        data,
    );

    return response.data.data;
}

export async function acceptAnswer(
    answerId: number,
): Promise<Answer> {
    const response = await api.post<ApiResponse<Answer>>(
        `/qa/answers/${answerId}/accept/`,
    );

    return response.data.data;
}

export async function toggleAnswerVote(
    answerId: number,
): Promise<VoteResult> {
    const response = await api.post<ApiResponse<VoteResult>>(
        `/qa/answers/${answerId}/vote/`,
    );

    return response.data.data;
}

export async function moderateQuestion(
    questionId: number,
    data: ModerationRequest,
): Promise<QuestionDetail> {
    const response = await api.patch<ApiResponse<QuestionDetail>>(
        `/qa/questions/${questionId}/moderate/`,
        data,
    );

    return response.data.data;
}

export async function moderateAnswer(
    answerId: number,
    data: ModerationRequest,
): Promise<Answer> {
    const response = await api.patch<ApiResponse<Answer>>(
        `/qa/answers/${answerId}/moderate/`,
        data,
    );

    return response.data.data;
}