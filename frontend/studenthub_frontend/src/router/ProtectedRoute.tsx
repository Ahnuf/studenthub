import { Navigate, Outlet } from "react-router-dom";
import { isAuthenticated } from "../api/tokenStorage";

// A "layout route" -- wrap any set of routes that require login
// as children of this one. If there's no access token, redirect
// to /login instead of rendering. If there is one, render the
// matched child route via <Outlet />.
export default function ProtectedRoute() {
    if (!isAuthenticated()) {
        return <Navigate to="/login" replace />;
    }

    return <Outlet />;
}
