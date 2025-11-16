# AeroShare 2.0 — Share Smarter. Anywhere.

AeroShare 2.0 is a lightweight, developer-friendly file sharing web app built with Flask. It enables quick peer-to-peer-style transfers via short share codes: a sender uploads a file and gets a 6-character code; a receiver uses that code to download the file. Designed for small-team demos, hackathons, and local file exchange without heavy infrastructure.

## Overview / Introduction

AeroShare 2.0 provides a minimal web UI and REST endpoints to upload files, generate a short share code, and allow recipients to download files using that code. It's perfect for fast, private, self-hosted file exchange when you don't want to rely on third-party file hosting or user accounts.

Why this exists
- Problem: Quick ad-hoc file transfers between nearby users often require cloud accounts or messy attachments.
- Value: Minimal setup, no external DB, short-lived share codes, and a clean UI for fast sharing.

## Features
- Upload files via a web UI and receive a 6-character share code.
- Retrieve files by entering a share code.
- Simple, responsive UI using Tailwind CSS (via CDN).
- Client-side JS for upload/receive flow and simulated progress.
- Saves uploads to a local `uploads/` directory.
- In-memory mapping of share codes to filenames (no external DB required).
- Lightweight, single-file Flask app ideal for local/offline usage.

## Tech Stack
- Python 3.x
- Flask (WSGI web framework)
- Tailwind CSS (via CDN) for UI
- Vanilla JavaScript for client interactions
- Local filesystem storage (`uploads/`)

## Architecture / System Design Overview

AeroShare is intentionally simple and runs as a single-process Flask server:

- Client (browser) -> POST `/upload` (multipart/form-data)
  - Server saves file to `uploads/`, generates a 6-character code and stores code→filename in memory.
- Client -> POST `/receive` with `{code}` to obtain a download URL.
- Client -> GET `/download/<code>` to download the file.

Simple ASCII flow:
```
[Browser Sender] --(POST /upload)--> [Flask Server: save file, code]
[Browser Recipient] --(POST /receive {code})--> [Flask Server: validate] --> {download_url}
[Browser Recipient] --(GET /download/<code>)--> [Flask Server: send file]
```

Notes:
- The current implementation keeps share codes in a Python dict (memory). Codes are ephemeral and will be lost on server restart.
- For production: add persistent storage, authentication, HTTPS, file size limits, and sanitization.

## Installation & Setup

Clone the repository and run locally.

Windows PowerShell:
```powershell
git clone https://github.com/himaparvathia23ec/AeroShare2.0.git
cd AeroShare2.0

# (recommended) create and activate a virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

pip install flask

# Run the app
python app.py
```

macOS / Linux:
```bash
git clone https://github.com/himaparvathia23ec/AeroShare2.0.git
cd AeroShare2.0
python3 -m venv .venv
source .venv/bin/activate
pip install flask
python app.py
```

Open: http://127.0.0.1:5000/

### Optional requirements file
Create `requirements.txt`:
```
Flask>=2.0
```
Install with `pip install -r requirements.txt`.

## Usage Instructions

1. Open the UI at `http://127.0.0.1:5000/`.
2. Click "Send File" or use the drag & drop area. After upload you'll receive a 6-character share code.
3. Share the code with the recipient.
4. The recipient clicks "Receive File", enters the code, and the browser will navigate to the download link.

Example using curl (upload):
```bash
curl -F "file=@/path/to/file.ext" http://127.0.0.1:5000/upload
# returns JSON like {"message":"Uploaded successfully","code":"ABC123"}
```

Example using curl (receive + download):
```bash
curl -X POST -H "Content-Type: application/json" -d '{"code":"ABC123"}' http://127.0.0.1:5000/receive
# returns {"message":"Ready to download","filename":"file.ext","download_url":"/download/ABC123"}

curl -OJ http://127.0.0.1:5000/download/ABC123
```

Notes:
- The app uses an in-memory `share_codes` mapping. Restarting the server clears codes.
- The front-end provides a user-friendly UI with a simulated progress bar.

## Folder Structure

```
.
├── app.py           # Main Flask application (routes + frontend HTML)
├── uploads/         # Saved uploaded files (created automatically)
├── README.md        # This file
└── PyCharmMiscProject.iml (IDE file)
```

## Contributing Guidelines

Contributions are welcome. Suggested workflow:

1. Fork the repo and create a feature branch: `git checkout -b feat/your-feature`
2. Make focused changes and include tests where applicable.
3. Open a PR describing the change and rationale.

Guidelines:
- Keep the core API stable or document breaking changes.
- For UI changes include screenshots or a short GIF.

## Future Improvements / Roadmap

- Add code expiry and automatic cleanup of the `uploads/` directory.
- Persist mapping to SQLite or Redis for robustness.
- Add optional end-to-end encryption for files.
- Add authentication, access control, and rate-limiting.
- Add chunked uploads & resume for large files.
- WebRTC-based direct peer-to-peer transfers to save server bandwidth.

## Team / Contributors

- Hima — project lead / backend + UI
- Contributors: add names and roles via PR

## License

This project is released under the MIT License. See `LICENSE` for details.

## Acknowledgments / Credits

- Flask — for the web framework
- Tailwind CSS — for the UI (via CDN)
- Browser APIs (FormData, fetch, navigator.clipboard) used by the client

---

If you'd like, I can also add a `requirements.txt`, a `LICENSE` file, a `CONTRIBUTING.md`, and a CI workflow. Tell me which you'd like next and I will add them and push.
# AeroShare2.0
