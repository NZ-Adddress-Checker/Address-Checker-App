import { useLogout } from "../hooks/useLogout";

export default function AccessDeniedPage({ username }) {
  const logout = useLogout();

  return (
    <main className="screen">
      <section className="card access-denied">
        <div className="access-denied-icon">⛔</div>
        <h1>Access Denied</h1>
        <p className="access-denied-message">
          Sorry{username ? `, ${username}` : ""}, you do not have permission to access the Address Validation feature.
        </p>
        <p className="access-denied-details">
          Please contact your administrator to request access to the <strong>AddressValidators</strong> group.
        </p>
        <button type="button" className="button" onClick={logout}>
          Logout
        </button>
      </section>
    </main>
  );
}
