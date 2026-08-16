import api from "./client";
import type { University, Program, AcademicSession } from "../types/academic";

export async function getUniversities(): Promise<University[]> {
    const response = await api.get<University[]>(
        "/academic/universities/",
    );

    return response.data;
}

export async function getPrograms(
    universityId: number,
): Promise<Program[]> {
    const response = await api.get<Program[]>(
        "/academic/programs/",
        { params: { university: universityId } },
    );

    return response.data;
}

export async function getSessions(
    universityId: number,
): Promise<AcademicSession[]> {
    const response = await api.get<AcademicSession[]>(
        "/academic/sessions/",
        { params: { university: universityId } },
    );

    return response.data;
}

export interface CourseOption {
    id: number;
    course: number;
    title: string;
    course_code: string;
    recommended_semester: number | null;
    category: string;
}

export async function getCourses(): Promise<CourseOption[]> {
    const response = await api.get<CourseOption[]>(
        "/academic/courses/",
    );

    return response.data;
}