import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import AddressChecker from './components/AddressChecker';
import Login from './components/Login';
import ProtectedRoute from './components/ProtectedRoute';
import { AuthProvider } from './context/AuthContext';
import GlobalStyle from './styles/GlobalStyles';

function App() {
  return (
    <>
      <GlobalStyle />
      <AuthProvider>
        <BrowserRouter>
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route
              path="/address-checker"
              element={
                <ProtectedRoute>
                  <AddressChecker />
                </ProtectedRoute>
              }
            />
            <Route path="/" element={<Navigate to="/address-checker" replace />} />
            <Route path="*" element={<Navigate to="/address-checker" replace />} />
          </Routes>
        </BrowserRouter>
      </AuthProvider>
    </>
  );
}

export default App;
