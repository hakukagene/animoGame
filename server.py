"""Compatibility entry point for existing Render Web Service settings."""

from voting_server.app import app


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
