export interface StudentProfileCreateRequest {
    university: number;
    program: number;
    joined_session: number;
    current_semester: number;
    registration_number?: string;
    roll_number?: string;
    expected_graduation_date: string; // "YYYY-MM-DD"
    academic_status?: string; // optional, backend defaults to ACTIVE
}

// Matches StudentProfileDetailSerializer, which is what the
// create view returns after a successful POST.
export interface StudentProfileData {
    id: number;
    university: number;
    university_name: string;
    program: number;
    program_name: string;
    joined_session: number;
    joined_session_name: string;
    current_semester: number;
    registration_number: string | null;
    roll_number: string | null;
    expected_graduation_date: string;
    academic_status: string;
}