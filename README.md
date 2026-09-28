# ManuScript

**ManuScript** is an intelligent academic manuscript formatting system that turns an unstructured research document into a consistent, submission-ready document.

## Current repository structure

- `frontend/` — polished, responsive browser workspace
  - `index.html` — application shell and workflow
  - `styles.css` — responsive dark interface and components
  - `app.js` — upload, style selection, API integration, results and document history
  - `README.md` — frontend setup and backend contract
- `test_*.py` — backend/API/feature regression tests
- `create_test_doc.py` — reusable DOCX fixture generator
- `test_manuscript.docx` and `informal_test.docx` — fixtures still referenced by the test suite

Generated outputs, duplicate document artifacts, and one-off diagnostic scripts are intentionally not tracked.

## Supported workflow

1. Upload a `.docx` manuscript.
2. Choose **IEEE**, **APA**, **MLA**, or **Standard** formatting.
3. Select Word or LaTeX output.
4. Send the document to the existing `POST /process` API.
5. Review returned statistics and quality insights.
6. Download the formatted result.
7. View recent documents through `GET /documents`.

## Frontend

The UI uses dependency-free HTML, CSS and JavaScript, so it does not introduce a second package/dependency tree into the repository.

To preview it locally:

```bash
python -m http.server 5173 --directory frontend
```

The frontend assumes the API is available at the same origin. If the API is hosted separately, set `API_BASE` in `frontend/app.js` and configure CORS on the backend.

## Important

The current public repository does **not** contain the backend implementation itself. The frontend therefore connects to the API contract already exercised by the repository's test suite rather than inventing backend functionality.

## Project goal

ManuScript focuses on removing repetitive academic formatting work while keeping the underlying document-processing workflow testable and extensible.
