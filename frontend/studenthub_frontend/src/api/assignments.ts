import api from "./client";
import type { ApiResponse } from "../types/auth";
import type {
    Assignment,
    AssignmentCreateRequest,
    AssignmentUpdateRequest,
} from "../types/assignment";

export async function listAssignments(): Promise<ApiResponse<Assignment[]>> {
    const response = await api.get<ApiResponse<Assignment[]>>("/assignments/");
    return response.data;
}

export async function createAssignment(
    data: AssignmentCreateRequest,
): Promise<ApiResponse<Assignment>> {
    const response = await api.post<ApiResponse<Assignment>>(
        "/assignments/",
        data,
    );
    return response.data;
}

export async function updateAssignment(
    id: number,
    data: AssignmentUpdateRequest,
): Promise<ApiResponse<Assignment>> {
    const response = await api.patch<ApiResponse<Assignment>>(
        `/assignments/${id}/`,
        data,
    );
    return response.data;
}

export async function deleteAssignment(id: number): Promise<void> {
    await api.delete(`/assignments/${id}/`);
}