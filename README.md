# Demo Python Flask App

Minimal Python Flask application used to demo a basic service:

- Run a local HTTP server
- Expose a single endpoint (`/`) that returns "Hello, world!"

The goal is to start simple and increment. 

---

## Prerequisites

- macOS (Apple Silicon)
- Python 3.10+
- VS Code (recommended)

---

## Installing Python (macOS)

The recommended way to install Python on macOS is via Homebrew.

If you do not have Homebrew installed:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Install Python:
```bash
brew install python
```

Verify installation:
```bash
python3 --version
```

### Setting up the virtual environment
Create a virtual environment in the project directory:
```bash
python3 -m venv .venv
```

Activate the virtual environment:
```bash
source .venv/bin/activate
```

Your shell prompt should now show that the virtual environment is active.

### Installing dependencies
With the virtual environment activated, install Flask:
```bash
pip install -r requirements.txt
```

Current project dependencies:

- Flask

### Running the application
Start the application:
```bash
python app.py
```

The server will start on port 8000.

Test it in another terminal:
```bash
curl http://localhost:8000/
```

Expected output:

```
Hello, world!
```

### Development notes
- This app uses Flask's built-in development server
- The server is configured to listen on `0.0.0.0:8000`
- Auto-reload is enabled via `debug=True`
