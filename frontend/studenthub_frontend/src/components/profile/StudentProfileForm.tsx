"use no memo";
// StudentProfileForm genuinely needs react-hook-form's watch()
// for its reactive behavior (re-fetching programs/sessions when
// the selected university changes) -- unlike RegisterForm's
// password-match check, there's no non-reactive substitute here,
// so this component is opted out of React Compiler's optimization
// rather than restructured around it.

import { useForm } from "react-hook-form";
import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import axios from "axios";
import { getUniversities, getPrograms, getSessions } from "../../api/academic";
import { createStudentProfile } from "../../api/studentProfile";
import type { University, Program, AcademicSession } from "../../types/academic";
import type { StudentProfileCreateRequest } from "../../types/studentProfile";

interface ApiErrorResponse {
    success: boolean;
    message: string;
}

export default function StudentProfileForm() {
    const navigate = useNavigate();

    const [universities, setUniversities] = useState<University[]>([]);
    const [programs, setPrograms] = useState<Program[]>([]);
    const [sessions, setSessions] = useState<AcademicSession[]>([]);
    const [serverError, setServerError] = useState<string | null>(null);
    const [isSubmitting, setIsSubmitting] = useState(false);

    const {
        register,
        handleSubmit,
        watch,
        setValue,
        formState: { errors },
    } = useForm<StudentProfileCreateRequest>();

    const selectedUniversity = watch("university");

    // Load universities once, on mount.
    useEffect(() => {
        getUniversities()
            .then((res) => {
                setUniversities(res);
            })
            .catch((error) => {
                console.error("Universities request failed:", error);
                setServerError("Failed to load universities.");
            });
    }, []);

    // Reactively reload programs/sessions whenever the selected
    // university changes -- this is the correct use of watch():
    // we WANT a re-render/effect on every change here, unlike a
    // one-off validate-time read (see RegisterForm's getValues()).
    useEffect(() => {
        if (!selectedUniversity) {
            setPrograms([]);
            setSessions([]);
            return;
        }

        // Clear any previously-selected program/session -- they
        // belonged to a different university and are no longer valid.
        setValue("program", undefined as unknown as number);
        setValue("joined_session", undefined as unknown as number);

        Promise.all([
            getPrograms(selectedUniversity),
            getSessions(selectedUniversity),
        ])
            .then(([programsRes, sessionsRes]) => {
                setPrograms(programsRes);
                setSessions(sessionsRes);
            })
            .catch(() => setServerError("Failed to load programs/sessions."));
    }, [selectedUniversity, setValue]);

    async function onSubmit(data: StudentProfileCreateRequest) {
        setServerError(null);
        setIsSubmitting(true);

        try {
            await createStudentProfile(data);
            navigate("/dashboard");
        } catch (err: unknown) {
            let message = "Failed to create profile. Please try again.";

            if (axios.isAxiosError<ApiErrorResponse>(err)) {
                message = err.response?.data?.message ?? message;
            }

            setServerError(message);
        } finally {
            setIsSubmitting(false);
        }
    }

    return (
        <form
            onSubmit={handleSubmit(onSubmit)}
            className="w-full max-w-lg space-y-4 rounded-lg bg-white p-8 shadow-sm"
        >
            <h1 className="mb-2 text-2xl font-semibold text-gray-900">
                Set up your student profile
            </h1>

            <div>
                <label className="mb-1 block text-sm font-medium text-gray-700">
                    University
                </label>
                <select
                    className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                    {...register("university", {
                        required: "Select a university",
                        valueAsNumber: true,
                    })}
                >
                    <option value="">Select a university</option>
                    {universities.map((u) => (
                        <option key={u.id} value={u.id}>
                            {u.name}
                        </option>
                    ))}
                </select>
                {errors.university && (
                    <p className="mt-1 text-sm text-red-600">
                        {errors.university.message}
                    </p>
                )}
            </div>

            <div>
                <label className="mb-1 block text-sm font-medium text-gray-700">
                    Program
                </label>
                <select
                    disabled={!selectedUniversity}
                    className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 disabled:bg-gray-100"
                    {...register("program", {
                        required: "Select a program",
                        valueAsNumber: true,
                    })}
                >
                    <option value="">
                        {selectedUniversity
                            ? "Select a program"
                            : "Select a university first"}
                    </option>
                    {programs.map((p) => (
                        <option key={p.id} value={p.id}>
                            {p.degree_type} — {p.program_name}
                        </option>
                    ))}
                </select>
                {errors.program && (
                    <p className="mt-1 text-sm text-red-600">
                        {errors.program.message}
                    </p>
                )}
            </div>

            <div>
                <label className="mb-1 block text-sm font-medium text-gray-700">
                    Joined Session
                </label>
                <select
                    disabled={!selectedUniversity}
                    className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 disabled:bg-gray-100"
                    {...register("joined_session", {
                        required: "Select a session",
                        valueAsNumber: true,
                    })}
                >
                    <option value="">
                        {selectedUniversity
                            ? "Select a session"
                            : "Select a university first"}
                    </option>
                    {sessions.map((s) => (
                        <option key={s.id} value={s.id}>
                            {s.display_name}
                        </option>
                    ))}
                </select>
                {errors.joined_session && (
                    <p className="mt-1 text-sm text-red-600">
                        {errors.joined_session.message}
                    </p>
                )}
            </div>

            <div>
                <label className="mb-1 block text-sm font-medium text-gray-700">
                    Current Semester
                </label>
                <input
                    type="number"
                    min={1}
                    max={12}
                    className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                    {...register("current_semester", {
                        required: "Current semester is required",
                        valueAsNumber: true,
                        min: { value: 1, message: "Must be between 1 and 12" },
                        max: { value: 12, message: "Must be between 1 and 12" },
                    })}
                />
                {errors.current_semester && (
                    <p className="mt-1 text-sm text-red-600">
                        {errors.current_semester.message}
                    </p>
                )}
            </div>

            <div>
                <label className="mb-1 block text-sm font-medium text-gray-700">
                    Expected Graduation Date
                </label>
                <input
                    type="date"
                    className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                    {...register("expected_graduation_date", {
                        required: "Expected graduation date is required",
                    })}
                />
                {errors.expected_graduation_date && (
                    <p className="mt-1 text-sm text-red-600">
                        {errors.expected_graduation_date.message}
                    </p>
                )}
            </div>

            <div className="flex gap-3">
                <div className="flex-1">
                    <label className="mb-1 block text-sm font-medium text-gray-700">
                        Registration No. (optional)
                    </label>
                    <input
                        type="text"
                        className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                        {...register("registration_number")}
                    />
                </div>
                <div className="flex-1">
                    <label className="mb-1 block text-sm font-medium text-gray-700">
                        Roll No. (optional)
                    </label>
                    <input
                        type="text"
                        className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                        {...register("roll_number")}
                    />
                </div>
            </div>

            {serverError && (
                <p className="text-sm text-red-600" role="alert">
                    {serverError}
                </p>
            )}

            <button
                type="submit"
                disabled={isSubmitting}
                className="w-full rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-60"
            >
                {isSubmitting ? "Creating profile..." : "Create Profile"}
            </button>
        </form>
    );
}
