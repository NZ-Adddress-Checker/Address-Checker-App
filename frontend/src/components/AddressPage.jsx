import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { checkAddress, getAddressSuggestions } from "../api";
import { buildAppLogoutUrl, clearAuthSession } from "../auth/index.js";
import { NZ_ADDRESS_SUGGESTIONS } from "../constants/addressSuggestions";
import { AUTH_MESSAGES } from "../constants/authMessages";
import { appConfig, isCognitoConfigured } from "../config";

function normalizeError(error) {
  if (error.response?.status === 401) {
    return AUTH_MESSAGES.invalidSession;
  }
  if (error.code === "ECONNABORTED") {
    return AUTH_MESSAGES.requestTimedOut;
  }
  if (error.response?.data?.detail) {
    return error.response.data.detail;
  }
  return AUTH_MESSAGES.addressValidationFailed;
}

export default function AddressPage() {
  const navigate = useNavigate();
  const [address, setAddress] = useState("");
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [addressSuggestions, setAddressSuggestions] = useState(NZ_ADDRESS_SUGGESTIONS);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const trimmedInput = address.trim().toLowerCase();
  const suggestions =
    trimmedInput.length < 2
      ? []
      : addressSuggestions.filter((item) => item.toLowerCase().includes(trimmedInput)).slice(0, 6);

  useEffect(() => {
    let isMounted = true;

    const loadSuggestions = async () => {
      try {
        const items = await getAddressSuggestions();
        if (isMounted && items.length > 0) {
          setAddressSuggestions(items);
        }
      } catch {
        // Keep local fallback suggestions if endpoint is unavailable.
      }
    };

    void loadSuggestions();
    return () => {
      isMounted = false;
    };
  }, []);

  const onLogout = () => {
    clearAuthSession();

    if (isCognitoConfigured()) {
      try {
        const logoutUrl = buildAppLogoutUrl({
          domain: appConfig.cognito.domain,
          clientId: appConfig.cognito.clientId,
          redirectUri: appConfig.cognito.redirectUri,
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
      setError(AUTH_MESSAGES.emptyAddress);
      return;
    }

    try {
      setLoading(true);
      const data = await checkAddress(address.trim());
      setResult(data);
      if (!data.is_valid) {
        setError(AUTH_MESSAGES.addressNotInSuggestions);
      }
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
              <strong>Source:</strong> {result.source}
            </p>
          </div>
        )}
      </section>
    </main>
  );
}
