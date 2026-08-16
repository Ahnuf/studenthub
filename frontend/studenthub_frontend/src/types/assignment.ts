export type AssignmentStatus = "PENDING" | "IN_PROGRESS" | "COMPLETED";

export interface Assignment {
    id: number;
    course_name: string;
    title: string;
    description: string;
    due_date: string; // "YYYY-MM-DD"
    status: AssignmentStatus;
    status_display: string;
    created_at: string;
    updated_at: string;
}

export interface AssignmentCreateRequest {
    course_name: string;
    title: string;
    description?: string;
    due_date: string;
}

export interface AssignmentUpdateRequest {
    course_name?: string;
    title?: string;
    description?: string;
    due_date?: string;
    status?: AssignmentStatus;
}