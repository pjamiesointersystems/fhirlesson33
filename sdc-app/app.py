
import os
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import json

ROOT = Path(__file__).parent.resolve()
STATIC_DIR = ROOT / "static"
FORMS_DIR = ROOT / "forms"   # <--- Put student-exported JSON files here

load_dotenv()
FHIR_BASE = os.getenv("FHIR_BASE", "http://localhost:8080/csp/healthshare/demo/fhir/r4")

# NEW: which form to display by default (students change this per their file)
FORM_FILE = os.getenv("FORM_FILE", "History-of-Tobacco-use.R4.json")

app = FastAPI(title="SDC Demo Server", version="1.1.0")

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/", response_class=HTMLResponse)
async def root_index():
    index_path = STATIC_DIR / "index.html"
    if not index_path.exists():
        raise HTTPException(status_code=404, detail="index.html not found")
    return FileResponse(index_path)


# NEW: return the Questionnaire JSON specified by FORM_FILE (or ?name=)
@app.get("/api/form")
async def get_form(name: str | None = None):
    """
    Serve a Questionnaire JSON from the /forms directory.
    - Default file comes from FORM_FILE env var.
    - Optional ?name=SomeFile.json lets you override per request.
    """
    file_name = name or FORM_FILE
    # prevent path escape
    candidate = (FORMS_DIR / file_name).resolve()
    if FORMS_DIR not in candidate.parents:
        raise HTTPException(status_code=400, detail="Invalid file name")

    if not candidate.exists():
        raise HTTPException(status_code=404, detail=f"Form not found: {file_name}")

    try:
        data = json.loads(candidate.read_text(encoding="utf-8"))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON: {e}")

    # lightweight sanity check
    if data.get("resourceType") != "Questionnaire":
        raise HTTPException(status_code=400, detail="File is not a FHIR Questionnaire")

    return JSONResponse(data)


# keep your earlier proxy endpoints, etc…


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",   # or "lp_server:app" if your module is named lp_server.py
        host="127.0.0.1",
        port=8888,
        reload=False,
        workers=1,
    )