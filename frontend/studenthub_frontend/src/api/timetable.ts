import api from "./client";

import type {
    TimetableCreateRequest,
    TimetableCreateResponse,
    TimetableEntry,
    TimetableListResponse,
    TimetableResponse,
    TimetableUpdateRequest,
} from "../types/timetable";

export async function getTimetable(): Promise<TimetableEntry[]> {
    const response = await api.get<TimetableListResponse>(
        "/timetable/",
    );

    return response.data.data;
}

export async function createTimetableEntry(
    data: TimetableCreateRequest,
): Promise<TimetableCreateResponse> {
    const response = await api.post<TimetableCreateResponse>(
        "/timetable/",
        data,
    );

    return response.data;
}

export async function updateTimetableEntry(
    entryId: number,
    data: TimetableUpdateRequest,
): Promise<TimetableEntry> {
    const response = await api.patch<TimetableResponse>(
        `/timetable/${entryId}/`,
        data,
    );

    return response.data.data;
}

export async function deleteTimetableEntry(
    entryId: number,
): Promise<void> {
    await api.delete(`/timetable/${entryId}/`);
}