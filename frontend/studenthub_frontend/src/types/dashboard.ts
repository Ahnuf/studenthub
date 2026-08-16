// Matches AcademicProgressDashboardSerializer exactly (built and
// verified earlier in this project's backend work).

export interface AcademicIdentity {
    university: string;
    program: string;
    current_semester: number;
    joined_session: string;
    academic_status: string;
    expected_graduation_date: string;
}

export interface CurrentCourse {
    course_code: string;
    course_title: string;
    credit_hours: number;
    status: string;
}

export interface CurrentSemester {
    current_courses: CurrentCourse[];
    current_credit_hours: number;
    semester_gpa: number;
}

export interface DegreeProgress {
    completed_credit_hours: number;
    remaining_credit_hours: number;
    completed_courses: number;
    remaining_courses: number;
    total_program_credit_hours: number;
    total_program_courses: number;
    progress_percentage: number;
}

export interface Performance {
    cgpa: number;
}

export interface AssignmentSummary {
    id: number;
    course_name: string;
    title: string;
    due_date: string;
    status: string;
}

export interface AssignmentsDueSoon {
    upcoming: AssignmentSummary[];
    overdue: AssignmentSummary[];
}

export interface TimetableTodayEntry {
    id: number;
    course_name: string;
    day_of_week_display: string;
    start_time: string;
    end_time: string;
    location: string;
}

export interface RecentNote {
    id: number;
    course_title: string;
    main_heading: string;
    sub_heading: string;
    uploaded_by: string;
    created_at: string;
}

export interface FlashcardsSummary {
    available_decks: number;
    cards_reviewed: number;
    cards_known: number;
}

export interface MyQuestion {
    id: number;
    course_title: string;
    title: string;
    answer_count: number;
    is_resolved: boolean;
    created_at: string;
}

export interface MyAnswer {
    id: number;
    question_title: string;
    body: string;
    is_accepted: boolean;
    vote_count: number;
    created_at: string;
}

export interface QAActivity {
    my_questions: MyQuestion[];
    my_answers: MyAnswer[];
}

export interface CourseAttendance {
    course_code: string;
    course_title: string;
    total_sessions: number;
    present_count: number;
    absent_count: number;
    leave_count: number;
    attendance_percentage: number;
}

export interface AttendanceOverview {
    overall_percentage: number;
    courses: CourseAttendance[];
    at_risk_courses: string[];
}

export interface AcademicProgressDashboard {
    academic_identity: AcademicIdentity;
    current_semester: CurrentSemester;
    degree_progress: DegreeProgress;
    performance: Performance;
    assignments_due_soon: AssignmentsDueSoon;
    timetable_today: TimetableTodayEntry[];
    recent_notes: RecentNote[];
    flashcards: FlashcardsSummary;
    qa_activity: QAActivity;
    attendance: AttendanceOverview;
}