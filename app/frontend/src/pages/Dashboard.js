import { useState, useRef, useEffect } from "react";
import { useAuth } from "react-oidc-context";
import api, { setAuthToken } from "../services/api";
import config from "../config";
import "./Dashboard.css";

export default function Dashboard() {
  const auth = useAuth();
  const [query, setQuery] = useState("");
  const [suggestions, setSuggestions] = useState([]);
  const [selectedAddress, setSelectedAddress] = useState(null);
  const [error, setError] = useState("");
  const [result, setResult] = useState(null);
  const debounceRef = useRef(null);

  useEffect(() => {
    setAuthToken(auth.user?.id_token ?? null);
  }, [auth.user]);

  const handleInput = (e) => {
    const val = e.target.value;
    setQuery(val);
    setSelectedAddress(null);
    setError("");
    setResult(null);

    if (debounceRef.current) clearTimeout(debounceRef.current);

    if (!val.trim()) {
      setSuggestions([]);
      return;
    }

    debounceRef.current = setTimeout(async () => {
      try {
        const res = await api.get(`/address/suggest?q=${encodeURIComponent(val)}`);
        const data = res.data;
        const items = Array.isArray(data) ? data : (data.completions || data.suggestions || data.results || []);
        setSuggestions(items);
      } catch (err) {
        if (err.response?.status === 401 || err.response?.status === 403) {
          setError("Session expired. Please log out and log in again.");
        } else if (err.response?.status === 502) {
          setError("Address lookup service is temporarily unavailable. Please try again later.");
        } else if (err.response) {
          setError(`Error: ${err.response.data?.detail || 'Unable to fetch suggestions'}`);
        } else {
          setError("Network error. Please check your connection.");
        }
        setSuggestions([]);
      }
    }, 300);
  };

  const handleSelect = (item) => {
    const addr = item.formatted || item.full_address || item.address || item.label || "";
    setQuery(addr);
    setSelectedAddress(item);
    setSuggestions([]);
    setError("");
  };

  const handleValidate = async () => {
    if (!selectedAddress) {
      setError("Please select an address from the dropdown list.");
      return;
    }
    try {
      const res = await api.post("/address/validate", { address: query });
      setResult(res.data);
      setError("");
    } catch (err) {
      if (err.response?.status === 401 || err.response?.status === 403) {
        setError("Session expired. Please log out and log in again.");
      } else {
        setError("Validation failed. Please try again.");
      }
    }
  };

  const handleLogout = () => {
    auth.removeUser();
    window.location.href = `${config.cognito.domain}/logout?client_id=${config.cognito.clientId}&logout_uri=${encodeURIComponent(config.cognito.logoutUri)}`;
  };

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <h2>Address Checker</h2>
        <button onClick={handleLogout}>Logout</button>
      </div>

      <div className="address-input-wrapper">
        <input
          className="address-input"
          value={query}
          onChange={handleInput}
          placeholder="Start typing an address..."
          autoComplete="off"
        />
        {suggestions.length > 0 && (
          <ul className="suggestions-list">
            {suggestions.map((item, i) => (
              <li
                key={item.formatted || item.pxid || i}
                className="suggestion-item"
                onClick={() => handleSelect(item)}
              >
                {item.formatted || item.full_address || item.address || item.label || JSON.stringify(item)}
              </li>
            ))}
          </ul>
        )}
      </div>

      <div className="validate-row">
        <button onClick={handleValidate}>Validate</button>
      </div>

      {error && <p className="error-message">{error}</p>}

      {result && result.valid && (
        <div className="result-container">
          <p className="result-valid">Valid: Yes ✓</p>
          {result.address && (
            <pre className="result-json">
              {JSON.stringify(result.address, null, 2)}
            </pre>
          )}
        </div>
      )}
    </div>
  );
}
