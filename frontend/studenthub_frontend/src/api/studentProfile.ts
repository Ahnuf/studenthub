import api from "./client";
import type { StudentProfileCreateRequest, StudentProfileData } from "../types/studentProfile";

// NOTE: unlike every other endpoint in this app, StudentProfileAPIView's
// POST (as last reviewed) returns a raw Response(...), NOT wrapped in
// the {success, message, data} envelope -- so response.data here IS
// the profile object directly, not response.data.data. Verify this
// is still accurate; if the backend gets fixed to use the standard
// envelope, this function needs `response.data.data` instead.
export async function createStudentProfile(
    data: StudentProfileCreateRequest,
): Promise<StudentProfileData> {
    const response = await api.post<StudentProfileData>(
        "/students/profile/",
        data,
    );
    return response.data;
}