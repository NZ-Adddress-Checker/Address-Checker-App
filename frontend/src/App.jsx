import { Navigate, Route, Routes } from "react-router-dom";
import CallbackPage from "./components/CallbackPage";
import AddressPage from "./components/AddressPage";
import LoginPage from "./components/LoginPage";
import ProtectedRoute from "./components/ProtectedRoute";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<LoginPage />} />
      <Route path="/callback" element={<CallbackPage />} />
      <Route
        path="/address"
        element={
          <ProtectedRoute>
            <AddressPage />
          </ProtectedRoute>
        }
      />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}
