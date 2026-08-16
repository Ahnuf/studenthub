import { Routes, Route } from "react-router-dom";
import Login from "../pages/Login";
import Register from "../pages/Register";
import Dashboard from "../pages/Dashboard";
import CreateProfile from "../pages/CreateProfile";
import Assignments from "../pages/Assignments";
import ProtectedRoute from "./ProtectedRoute";
import AppShell from "../components/layout/AppShell";
import Timetable from "../pages/Timetable";
import Notes from "../pages/Notes";
import NoteDetail from "../pages/NoteDetail";
import QA from "../pages/QA";
import Flashcards from "../pages/Flashcards";
import FlashcardDeck from "../pages/FlashcardDeck";

export default function AppRouter() {
    return (
        <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/notes" element={<Notes />} />
            <Route path="/notes/:noteId" element={<NoteDetail />}/>
            <Route path="/qa" element={<QA />} />
            <Route path="/flashcards" element={<Flashcards />} />
            <Route path="/flashcards/decks/:deckId" element={<FlashcardDeck />}/>

            <Route element={<ProtectedRoute />}>
                <Route path="/profile/create" element={<CreateProfile />} />

                <Route element={<AppShell />}>
                    <Route path="/dashboard" element={<Dashboard />} />
                    <Route path="/assignments" element={<Assignments />} />
                    <Route path="/timetable" element={<Timetable />} />
                    {/* Notes, Flashcards, Quizzes, QA go here next */}
                </Route>
            </Route>
        </Routes>
    );
}