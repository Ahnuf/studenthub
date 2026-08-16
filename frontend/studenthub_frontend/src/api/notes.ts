import api from "./client";

import type {
    Note,
    NoteCreateRequest,
    NoteUpdateRequest,
} from "../types/notes";

interface ApiResponse<T> {
    success: boolean;
    message: string;
    data: T;
}

function buildNoteFormData(data: NoteCreateRequest): FormData {
    const formData = new FormData();

    formData.append("course", String(data.course));
    formData.append("main_heading", data.main_heading);

    if (data.sub_heading) {
        formData.append("sub_heading", data.sub_heading);
    }

    if (data.description) {
        formData.append("description", data.description);
    }

    formData.append("file", data.file);

    return formData;
}

function buildNoteUpdateFormData(data: NoteUpdateRequest): FormData {
    const formData = new FormData();

    if (data.main_heading !== undefined) {
        formData.append("main_heading", data.main_heading);
    }

    if (data.sub_heading !== undefined) {
        formData.append("sub_heading", data.sub_heading);
    }

    if (data.description !== undefined) {
        formData.append("description", data.description);
    }

    if (data.file !== undefined) {
        formData.append("file", data.file);
    }

    return formData;
}

export async function getNotes(
    courseId?: number,
    query?: string,
): Promise<Note[]> {
    const response = await api.get<ApiResponse<Note[]>>(
        "/notes/",
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

export async function getNote(noteId: number): Promise<Note> {
    const response = await api.get<ApiResponse<Note>>(
        `/notes/${noteId}/`,
    );

    return response.data.data;
}

export async function createNote(
    data: NoteCreateRequest,
): Promise<Note> {
    const response = await api.post<ApiResponse<Note>>(
        "/notes/",
        buildNoteFormData(data),
    );

    return response.data.data;
}

export async function updateNote(
    noteId: number,
    data: NoteUpdateRequest,
): Promise<Note> {
    const response = await api.patch<ApiResponse<Note>>(
        `/notes/${noteId}/`,
        buildNoteUpdateFormData(data),
    );

    return response.data.data;
}

export async function deleteNote(noteId: number): Promise<void> {
    await api.delete(`/notes/${noteId}/`);
}