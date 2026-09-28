# ManuScript Frontend

A dependency-free responsive workspace for ManuScript. It uses plain HTML, CSS and JavaScript so the UI can be served without adding a frontend dependency tree.

## Backend contract

The UI expects:
- POST /process with file, style and output_format
- GET /documents for recent document history

The processing response can expose stats, download_url and quality_report.

## Run locally

Serve the frontend directory with any static server, for example:
python -m http.server 5173 --directory frontend

If the API is hosted separately, set API_BASE in app.js to its origin and enable the appropriate CORS policy on the backend.