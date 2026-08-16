import api from "./client";
import type { ApiResponse } from "../types/auth";
import type { AcademicProgressDashboard } from "../types/dashboard";

export async function getDashboard(): Promise<ApiResponse<AcademicProgressDashboard>> {
    const response = await api.get<ApiResponse<AcademicProgressDashboard>>(
        "/students/me/academic-progress/",
    );

    return response.data;
}