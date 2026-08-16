"use client";

import { useEffect, useState } from "react";
import ProtectedRoute from "@/components/ProtectedRoute";
import CourseTag from "@/components/CourseTag";
import { courseColor } from "@/lib/course-colors";
import { apiFetch, ApiError } from "@/lib/api";
import { useAuth } from "@/lib/auth-context";

interface CurrentCourse {
  course_code: string;
  course_title: string;
  credit_hours: number;
  status: string;
}

interface DashboardData {
  academic_identity: {
    university: string;
    program: string;
    current_semester: number;
    joined_session: string;
    academic_status: string;
    expected_graduation_date: string;
  };
  current_semester: {
    current_courses: CurrentCourse[];
    current_credit_hours: number;
    semester_gpa: string;
  };
  degree_progress: {
    completed_credit_hours: number;
    remaining_credit_hours: number;
    completed_courses: number;
    remaining_courses: number;
    total_program_credit_hours: number;
    total_program_courses: number;
    progress_percentage: string;
  };
  performance: {
    cgpa: string;
  };
  assignments_due_soon: {
    upcoming: Array<{
      id: number;
      course_name: string;
      title: string;
      due_date: string;
      status: string;
    }>;
    overdue: Array<{
      id: number;
      course_name: string;
      title: string;
      due_date: string;
      status: string;
    }>;
  };
}

export default function DashboardPage() {
  return (
    <ProtectedRoute>
      <DashboardContent />
    </ProtectedRoute>
  );
}

function DashboardContent() {
  const { user, logout } = useAuth();
  const [data, setData] = useState<DashboardData | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    apiFetch<DashboardData>("/students/academic-progress/")
      .then(setData)
      .catch((err) =>
        setError(
          err instanceof ApiError
            ? err.message
            : "Couldn't load your dashboard."
        )
      );
  }, []);

  if (error) {
    return (
      <div style={{ padding: 40 }}>
        <p className="form-error">{error}</p>
      </div>
    );
  }

  if (!data) {
    return <div style={{ padding: 40, color: "var(--ink-soft)" }}>Loading\u2026</div>;
  }

  const { academic_identity, current_semester, degree_progress, performance, assignments_due_soon } =
    data;

  return (
    <div className="dashboard-shell">
      <aside className="course-rail">
        <div className="course-rail-title">Your Courses</div>
        {current_semester.current_courses.map((course) => (
          <CourseTag
            key={course.course_code}
            courseKey={course.course_code}
            label={course.course_code}
          />
        ))}

        <div style={{ marginTop: 40 }}>
          <button
            onClick={() => logout()}
            style={{
              background: "none",
              border: "none",
              color: "var(--ink-soft)",
              cursor: "pointer",
              fontSize: "0.85rem",
              padding: 0,
            }}
          >
            Sign out
          </button>
        </div>
      </aside>

      <main className="dashboard-main">
        <div className="auth-eyebrow">
          {academic_identity.university} &middot; {academic_identity.program}
        </div>
        <h1>
          Welcome back{user?.first_name ? `, ${user.first_name}` : ""}
        </h1>

        <section className="dashboard-section">
          <div className="dashboard-section-label">This Semester</div>
          <div className="card-row">
            <div className="stat-card">
              <div className="stat-card-label">CGPA</div>
              <div className="stat-card-value numeric">{performance.cgpa}</div>
            </div>
            <div className="stat-card">
              <div className="stat-card-label">Semester GPA</div>
              <div className="stat-card-value numeric">
                {current_semester.semester_gpa}
              </div>
            </div>
            <div className="stat-card">
              <div className="stat-card-label">Credit Hours (Current)</div>
              <div className="stat-card-value numeric">
                {current_semester.current_credit_hours}
              </div>
            </div>
            <div className="stat-card">
              <div className="stat-card-label">Degree Progress</div>
              <div className="stat-card-value numeric">
                {degree_progress.progress_percentage}%
              </div>
            </div>
          </div>
        </section>

        {(assignments_due_soon.overdue.length > 0 ||
          assignments_due_soon.upcoming.length > 0) && (
          <section className="dashboard-section">
            <div className="dashboard-section-label">Due Soon</div>
            <div className="card-row">
              {assignments_due_soon.overdue.map((item) => (
                <div
                  key={`overdue-${item.id}`}
                  className="course-card"
                  style={{ borderLeftColor: "var(--danger)" }}
                >
                  <div className="course-card-heading">
                    <strong>{item.title}</strong>
                    <span className="course-card-code">{item.due_date}</span>
                  </div>
                  <div style={{ color: "var(--danger)", fontSize: "0.85rem" }}>
                    Overdue &middot; {item.course_name}
                  </div>
                </div>
              ))}

              {assignments_due_soon.upcoming.map((item) => (
                <div
                  key={`upcoming-${item.id}`}
                  className="course-card"
                  style={{ borderLeftColor: courseColor(item.course_name) }}
                >
                  <div className="course-card-heading">
                    <strong>{item.title}</strong>
                    <span className="course-card-code">{item.due_date}</span>
                  </div>
                  <div style={{ color: "var(--ink-soft)", fontSize: "0.85rem" }}>
                    {item.course_name}
                  </div>
                </div>
              ))}
            </div>
          </section>
        )}

        <section className="dashboard-section">
          <div className="dashboard-section-label">Your Courses This Semester</div>
          <div className="card-row">
            {current_semester.current_courses.map((course) => (
              <div
                key={course.course_code}
                className="course-card"
                style={{ borderLeftColor: courseColor(course.course_code) }}
              >
                <div className="course-card-heading">
                  <strong>{course.course_title}</strong>
                  <span className="course-card-code">{course.course_code}</span>
                </div>
                <div style={{ color: "var(--ink-soft)", fontSize: "0.85rem" }}>
                  {course.credit_hours} credit hours &middot; {course.status}
                </div>
              </div>
            ))}
          </div>
        </section>
      </main>
    </div>
  );
}
