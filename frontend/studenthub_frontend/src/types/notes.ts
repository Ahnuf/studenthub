export interface Note {
    id: number;
    course: number;
    course_title: string;
    main_heading: string;
    sub_heading: string;
    description: string;
    file: string;
    uploaded_by: string;
    created_at: string;
    updated_at: string;
}

export interface NoteCreateRequest {
    course: number;
    main_heading: string;
    sub_heading?: string;
    description?: string;
    file: File;
}

export interface NoteUpdateRequest {
    main_heading?: string;
    sub_heading?: string;
    description?: string;
    file?: File;
}