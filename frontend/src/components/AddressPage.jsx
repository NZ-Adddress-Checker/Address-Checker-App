import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { checkAddress } from "../api";
import { buildCognitoLogoutUrl, clearPkceState, clearToken } from "../auth";
import { appConfig, isCognitoConfigured } from "../config";

const NZ_ADDRESS_SUGGESTIONS = [
  "10 Queen Street, Auckland 1010",
  "120 Queen Street, Auckland 1010",
  "1 Viaduct Harbour Avenue, Auckland 1010",
  "34 Customs Street West, Auckland 1010",
  "167 Victoria Street West, Auckland 1010",
  "2 Quay Street, Auckland 1010",
  "1 Queen Street, Auckland 1010",
  "100 Lambton Quay, Wellington 6011",
  "25 Cuba Street, Wellington 6011",
  "15 Courtenay Place, Wellington 6011",
  "150 Willis Street, Wellington 6011",
  "1 Cathedral Square, Christchurch 8011",
  "120 Hereford Street, Christchurch 8011",
  "200 Colombo Street, Christchurch 8011",
  "8 The Octagon, Dunedin 9016",
  "70 George Street, Dunedin 9016",
  "45 Cameron Road, Tauranga 3110",
  "67 Victoria Street, Hamilton 3204",
  "3 Marine Parade, Napier 4110",
  "20 Trafalgar Street, Nelson 7010",
];

function normalizeError(error) {
  if (error.response?.status === 401) {
    return "Your session is invalid or expired. Please log in again.";
  }
  if (error.code === "ECONNABORTED") {
    return "The validation request timed out. Try again.";
  }
  if (error.response?.data?.detail) {
    return error.response.data.detail;
  }
  return "Address validation failed. Please try again.";
}

export default function AddressPage() {
  const navigate = useNavigate();
  const [address, setAddress] = useState("");
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const trimmedInput = address.trim().toLowerCase();
  const suggestions =
    trimmedInput.length < 2
      ? []
      : NZ_ADDRESS_SUGGESTIONS.filter((item) => item.toLowerCase().includes(trimmedInput)).slice(0, 6);

  const onLogout = () => {
    clearPkceState();
    clearToken();

    if (isCognitoConfigured()) {
      try {
        const redirectUrl = new URL(appConfig.cognito.redirectUri);
        const logoutUri = `${redirectUrl.origin}/`;
        const logoutUrl = buildCognitoLogoutUrl({
          domain: appConfig.cognito.domain,
          clientId: appConfig.cognito.clientId,
          logoutUri,
        });
        window.location.assign(logoutUrl);
        return;
      } catch {
        // Fall back to local logout if Cognito logout URL cannot be built.
      }
    }

    navigate("/", { replace: true });
  };

  const onSubmit = async (event) => {
    event.preventDefault();
    setError("");
    setResult(null);

    if (!address.trim()) {
      setError("Please enter an address.");
      return;
    }

    try {
      setLoading(true);
      const data = await checkAddress(address.trim());
      setResult(data);
      setShowSuggestions(false);
    } catch (err) {
      setError(normalizeError(err));
    } finally {
      setLoading(false);
    }
  };

  const onAddressChange = (value) => {
    setAddress(value);
    setShowSuggestions(true);
  };

  const onSelectSuggestion = (value) => {
    setAddress(value);
    setShowSuggestions(false);
  };

  return (
    <main className="screen">
      <section className="card">
        <div className="row-between">
          <h1>Address Validation</h1>
          <button type="button" className="button secondary" onClick={onLogout}>
            Logout
          </button>
        </div>

        <form onSubmit={onSubmit} className="form">
          <label htmlFor="address">NZ Address</label>
          <div className="autocomplete">
            <input
              id="address"
              name="address"
              value={address}
              onChange={(event) => onAddressChange(event.target.value)}
              onFocus={() => setShowSuggestions(true)}
              onBlur={() => setTimeout(() => setShowSuggestions(false), 120)}
              placeholder="10 Queen Street, Auckland"
              autoComplete="off"
            />
            {showSuggestions && suggestions.length > 0 && (
              <ul className="suggestions" role="listbox" aria-label="NZ address suggestions">
                {suggestions.map((item) => (
                  <li key={item}>
                    <button
                      type="button"
                      className="suggestion-item"
                      onMouseDown={(event) => event.preventDefault()}
                      onClick={() => onSelectSuggestion(item)}
                    >
                      {item}
                    </button>
                  </li>
                ))}
              </ul>
            )}
          </div>
          <button type="submit" className="button" disabled={loading}>
            {loading ? "Checking..." : "Validate"}
          </button>
        </form>

        {error && <p className="error">{error}</p>}

        {result && (
          <div className="result">
            <p>
              <strong>Valid:</strong> {result.is_valid ? "Yes" : "No"}
            </p>
            <p>
              <strong>Normalized:</strong> {result.normalized_address || "N/A"}
            </p>
            <p>
              <strong>Source:</strong> {result.source}
            </p>
          </div>
        )}
      </section>
    </main>
  );
}
