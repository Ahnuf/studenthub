import { Outlet, Link, useNavigate } from "react-router-dom";
import { logout as logoutApi } from "../../api/auth";
import { getRefreshToken, clearTokens } from "../../api/tokenStorage";

export default function AppShell() {
    const navigate = useNavigate();

    async function handleLogout() {
        const refreshToken = getRefreshToken();

        try {
            if (refreshToken) {
                await logoutApi(refreshToken);
            }
        } catch {
            // Even if the backend call fails (e.g. token already
            // expired), still log the user out locally -- no
            // reason to trap them in a broken session over it.
        } finally {
            clearTokens();
            navigate("/login");
        }
    }

    return (
        <div className="min-h-screen bg-gray-50">
            <header className="border-b border-gray-200 bg-white">
                <div className="mx-auto flex max-w-5xl items-center justify-between px-6 py-4">
                    <Link
                        to="/dashboard"
                        className="text-lg font-semibold text-gray-900"
                    >
                        StudentHub
                    </Link>

                    <nav className="flex items-center gap-6">
                        <Link
                            to="/dashboard"
                            className="text-sm text-gray-600 hover:text-gray-900"
                        >
                            Dashboard
                        </Link>

                        <Link
                            to="/assignments"
                            className="text-sm text-gray-600 hover:text-gray-900"
                        >
                            Assignments
                        </Link>

                        <Link
                            to="/notes"
                            className="text-sm text-gray-600 hover:text-gray-900"
                        >
                            Notes
                        </Link>

                        <Link
                            to="/qa"
                            className="text-sm text-gray-600 hover:text-gray-900"
                        >
                            Q&amp;A
                        </Link>

                        <Link
                            to="/flashcards"
                            className="text-sm text-gray-600 hover:text-gray-900"
                        >
                            Flashcards
                        </Link>

                        <Link
                            to="/timetable"
                            className="text-sm text-gray-600 hover:text-gray-900"
                        >
                            Timetable
                        </Link>

                        {/* Add more links here as their pages get built:
                            Notes, Flashcards, Quizzes, Q&A */}

                        <button
                            onClick={handleLogout}
                            className="rounded-md bg-gray-100 px-3 py-1.5 text-sm font-medium text-gray-700 hover:bg-gray-200"
                        >
                            Logout
                        </button>
                    </nav>
                </div>
            </header>

            <main>
                <Outlet />
            </main>
        </div>
    );
}