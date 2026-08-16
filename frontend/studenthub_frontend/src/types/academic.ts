export interface University {
    id: number;
    name: string;
    short_name: string;
    country: string;
    province: string;
    city: string;
}

export interface Program {
    id: number;
    university: number;
    degree_type: string;
    program_name: string;
    duration_years: number;
    study_system: string;
}

export interface AcademicSession {
    id: number;
    university: number;
    term: string;
    year: number;
    display_name: string;
    is_current: boolean;
}