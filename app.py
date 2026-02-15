"""
Minimal Flask hello-world application.

This is the first step toward a demo service.
For now, it only proves that:
- Python can run an HTTP server
- We can handle a request and return a response

Later commits will add:
- Multiple endpoints
- Mutable application state
- OpenTelemetry metrics
"""

from flask import Flask

# Create the Flask application object
app = Flask(__name__)


@app.route("/")
def hello():
    """
    Handle HTTP GET requests to "/".
    For now, just return a plain-text response.
    """
    return "Hello, world!"


if __name__ == "__main__":
    # Run the development server.
    # host="0.0.0.0" allows access from outside the machine (e.g. Docker).
    # debug=True enables auto-reload on code changes.
    app.run(host="0.0.0.0", port=8000, debug=True)
