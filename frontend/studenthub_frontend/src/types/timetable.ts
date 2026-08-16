export interface TimetableEntry {
    id: number;
    course_name: string;
    day_of_week: number;
    day_of_week_display: string;
    start_time: string;
    end_time: string;
    location: string;
    created_at: string;
    updated_at: string;
}

export interface TimetableCreateRequest {
    course_name: string;
    day_of_week: number;
    start_time: string;
    end_time: string;
    location?: string;
}

export interface TimetableUpdateRequest {
    course_name?: string;
    day_of_week?: number;
    start_time?: string;
    end_time?: string;
    location?: string;
}

export interface TimetableWarning {
    type?: string;
    message: string;
}

export interface TimetableResponse {
    success: boolean;
    message: string;
    data: TimetableEntry;
}

export interface TimetableListResponse {
    success: boolean;
    message: string;
    data: TimetableEntry[];
}

export interface TimetableCreateResponse {
    success: boolean;
    message: string;
    data: TimetableEntry;
    warnings?: TimetableWarning[];
}