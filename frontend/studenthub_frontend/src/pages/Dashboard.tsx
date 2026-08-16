import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import axios from "axios";
import { getDashboard } from "../api/dashboard";
import type { AcademicProgressDashboard } from "../types/dashboard";

interface ApiErrorResponse {
    success: boolean;
    message: string;
}

export default function Dashboard() {
    const [data, setData] = useState<AcademicProgressDashboard | null>(null);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [needsProfile, setNeedsProfile] = useState(false);

    useEffect(() => {
        async function fetchDashboard() {
            try {
                const response = await getDashboard();
                setData(response.data);
            } catch (err: unknown) {
                if (axios.isAxiosError<ApiErrorResponse>(err)) {
                    if (err.response?.status === 404) {
                        // Backend raises NotFound when the user
                        // hasn't created a StudentProfile yet.
                        setNeedsProfile(true);
                    } else {
                        setError(
                            err.response?.data?.message ??
                                "Failed to load dashboard.",
                        );
                    }
                } else {
                    setError("Failed to load dashboard.");
                }
            } finally {
                setIsLoading(false);
            }
        }

        fetchDashboard();
    }, []);

    if (isLoading) {
        return (
            <div className="flex items-center justify-center py-24">
                <p className="text-gray-500">Loading your dashboard...</p>
            </div>
        );
    }

    if (needsProfile) {
        return (
            <div className="flex items-center justify-center py-24">
                <div className="max-w-md rounded-lg bg-white p-8 text-center shadow-sm">
                    <h2 className="mb-2 text-lg font-semibold text-gray-900">
                        Complete your profile
                    </h2>
                    <p className="text-sm text-gray-600">
                        You need to set up your student profile
                        (university, program, session) before your
                        dashboard can show anything.
                    </p>
                    <Link
                        to="/profile/create"
                        className="mt-4 inline-block rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700"
                    >
                        Set up profile
                    </Link>
                </div>
            </div>
        );
    }

    if (error || !data) {
        return (
            <div className="flex items-center justify-center py-24">
                <p className="text-red-600">{error ?? "Something went wrong."}</p>
            </div>
        );
    }

    return (
        <div className="p-6">
            <div className="mx-auto max-w-5xl space-y-6">
                {/* Academic Identity */}
                <section className="rounded-lg bg-white p-6 shadow-sm">
                    <h2 className="mb-1 text-xl font-semibold text-gray-900">
                        {data.academic_identity.university}
                    </h2>
                    <p className="text-gray-600">
                        {data.academic_identity.program} · Semester{" "}
                        {data.academic_identity.current_semester}
                    </p>
                    <p className="mt-1 text-sm text-gray-500">
                        {data.academic_identity.academic_status} · Joined{" "}
                        {data.academic_identity.joined_session} · Expected
                        graduation{" "}
                        {new Date(
                            data.academic_identity.expected_graduation_date,
                        ).toLocaleDateString()}
                    </p>
                </section>

                {/* Top stats row */}
                <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
                    <StatCard label="CGPA" value={data.performance.cgpa.toFixed(2)} />
                    <StatCard
                        label="Semester GPA"
                        value={data.current_semester.semester_gpa.toFixed(2)}
                    />
                    <StatCard
                        label="Degree Progress"
                        value={`${data.degree_progress.progress_percentage}%`}
                    />
                    <StatCard
                        label="Attendance"
                        value={`${data.attendance.overall_percentage}%`}
                        warn={data.attendance.at_risk_courses.length > 0}
                    />
                </div>

                {/* Current Courses */}
                <section className="rounded-lg bg-white p-6 shadow-sm">
                    <h3 className="mb-3 font-semibold text-gray-900">
                        Current Courses ({data.current_semester.current_credit_hours} credit hours)
                    </h3>
                    {data.current_semester.current_courses.length === 0 ? (
                        <p className="text-sm text-gray-500">
                            No current enrollment found.
                        </p>
                    ) : (
                        <ul className="divide-y divide-gray-100">
                            {data.current_semester.current_courses.map((course) => (
                                <li
                                    key={course.course_code}
                                    className="flex justify-between py-2 text-sm"
                                >
                                    <span>
                                        {course.course_code} — {course.course_title}
                                    </span>
                                    <span className="text-gray-500">
                                        {course.credit_hours} cr
                                    </span>
                                </li>
                            ))}
                        </ul>
                    )}
                </section>

                {/* Today's Timetable + Assignments Due Soon, side by side */}
                <div className="grid gap-6 md:grid-cols-2">
                    <section className="rounded-lg bg-white p-6 shadow-sm">
                        <h3 className="mb-3 font-semibold text-gray-900">
                            Today's Classes
                        </h3>
                        {data.timetable_today.length === 0 ? (
                            <p className="text-sm text-gray-500">
                                Nothing scheduled today.
                            </p>
                        ) : (
                            <ul className="space-y-2">
                                {data.timetable_today.map((entry) => (
                                    <li key={entry.id} className="text-sm">
                                        <span className="font-medium">
                                            {entry.start_time}–{entry.end_time}
                                        </span>{" "}
                                        {entry.course_name}
                                        {entry.location && ` (${entry.location})`}
                                    </li>
                                ))}
                            </ul>
                        )}
                    </section>

                    <section className="rounded-lg bg-white p-6 shadow-sm">
                        <h3 className="mb-3 font-semibold text-gray-900">
                            Assignments Due Soon
                        </h3>
                        {data.assignments_due_soon.overdue.length > 0 && (
                            <div className="mb-3">
                                <p className="mb-1 text-xs font-medium uppercase text-red-600">
                                    Overdue
                                </p>
                                {data.assignments_due_soon.overdue.map((a) => (
                                    <p key={a.id} className="text-sm text-red-700">
                                        {a.title} ({a.course_name})
                                    </p>
                                ))}
                            </div>
                        )}
                        {data.assignments_due_soon.upcoming.length === 0 ? (
                            <p className="text-sm text-gray-500">
                                Nothing due in the next 7 days.
                            </p>
                        ) : (
                            data.assignments_due_soon.upcoming.map((a) => (
                                <p key={a.id} className="text-sm">
                                    {a.title} ({a.course_name}) — due{" "}
                                    {new Date(a.due_date).toLocaleDateString()}
                                </p>
                            ))
                        )}
                    </section>
                </div>

                {/* Recent Notes, Flashcards, QA — bottom row */}
                <div className="grid gap-6 md:grid-cols-3">
                    <section className="rounded-lg bg-white p-6 shadow-sm">
                        <h3 className="mb-3 font-semibold text-gray-900">
                            Recent Notes
                        </h3>
                        {data.recent_notes.length === 0 ? (
                            <p className="text-sm text-gray-500">
                                No notes for your courses yet.
                            </p>
                        ) : (
                            data.recent_notes.map((note) => (
                                <p key={note.id} className="mb-1 text-sm">
                                    {note.main_heading}
                                </p>
                            ))
                        )}
                    </section>

                    <section className="rounded-lg bg-white p-6 shadow-sm">
                        <h3 className="mb-3 font-semibold text-gray-900">
                            Flashcards
                        </h3>
                        <p className="text-sm text-gray-600">
                            {data.flashcards.available_decks} decks available
                        </p>
                        <p className="text-sm text-gray-600">
                            {data.flashcards.cards_known} of{" "}
                            {data.flashcards.cards_reviewed} cards known
                        </p>
                    </section>

                    <section className="rounded-lg bg-white p-6 shadow-sm">
                        <h3 className="mb-3 font-semibold text-gray-900">
                            Your Q&amp;A Activity
                        </h3>
                        <p className="text-sm text-gray-600">
                            {data.qa_activity.my_questions.length} questions asked
                        </p>
                        <p className="text-sm text-gray-600">
                            {data.qa_activity.my_answers.length} answers given
                        </p>
                    </section>
                </div>
            </div>
        </div>
    );
}

function StatCard({
    label,
    value,
    warn,
}: {
    label: string;
    value: string;
    warn?: boolean;
}) {
    return (
        <div className="rounded-lg bg-white p-4 shadow-sm">
            <p className="text-xs uppercase text-gray-500">{label}</p>
            <p
                className={`text-2xl font-semibold ${
                    warn ? "text-red-600" : "text-gray-900"
                }`}
            >
                {value}
            </p>
        </div>
    );
}
