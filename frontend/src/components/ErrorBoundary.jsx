import { Component } from "react";
import PropTypes from "prop-types";

export default class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, message: "" };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, message: error?.message || "Unknown error" };
  }

  componentDidCatch(error, info) {
    console.error("[ErrorBoundary]", error, info);
  }

  render() {
    if (this.state.hasError) {
      return (
        <main className="screen">
          <section className="card">
            <h1>Something went wrong</h1>
            <p className="error">{this.state.message}</p>
            <button
              type="button"
              className="button"
              onClick={() => window.location.assign("/")}
            >
              Go to Home
            </button>
          </section>
        </main>
      );
    }
    return this.props.children;
  }
}

ErrorBoundary.propTypes = {
  children: PropTypes.node.isRequired,
};
