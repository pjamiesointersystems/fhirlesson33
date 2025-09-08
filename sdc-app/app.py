
import os
import base64
import httpx
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi import Request
from dotenv import load_dotenv
import json

ROOT = Path(__file__).parent.resolve()
STATIC_DIR = ROOT / "static"
FORMS_DIR = ROOT / "forms"   # <--- Put student-exported JSON files here

load_dotenv()
FHIR_BASE = os.getenv("FHIR_BASE", "http://localhost:8080/csp/healthshare/demo/fhir/r4")


AUTH_HEADER = os.getenv("FHIR_AUTH_HEADER")
if not AUTH_HEADER:
    user = os.getenv("FHIR_BASIC_USER")
    pwd = os.getenv("FHIR_BASIC_PASS")
    if user and pwd:
        b64 = base64.b64encode(f"{user}:{pwd}".encode("utf-8")).decode("ascii")
        AUTH_HEADER = f"Basic {b64}"


# NEW: which form to display by default (students change this per their file)
FORM_FILE = os.getenv("FORM_FILE", "Smoking-Status.R4.json")

app = FastAPI(title="SDC Demo Server", version="1.1.0")

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

def _target_url(path: str, query: str) -> str:
    return f"{FHIR_BASE}/{path}{f'?{query}' if query else ''}"

def _proxy_headers(orig_ct: str | None = None) -> dict:
    # Force FHIR content types; you can relax this if you proxy other media.
    h = {
        "Accept": "application/fhir+json",
        "Content-Type": orig_ct or "application/fhir+json",
        "Prefer": "return=representation",  
    }
    if AUTH_HEADER:
        h["Authorization"] = AUTH_HEADER
    return h

@app.get("/api/fhir/{path:path}")
async def fhir_proxy_get(path: str, request: Request):
    url = _target_url(path, str(request.query_params))
    async with httpx.AsyncClient(timeout=30.0) as client:
        r = await client.get(url, headers=_proxy_headers())
    return Response(content=r.content, status_code=r.status_code,
                    media_type=r.headers.get("content-type", "application/fhir+json"))

@app.post("/api/fhir/{path:path}")
async def fhir_proxy_post(path: str, request: Request):
    url = _target_url(path, str(request.query_params))
    body = await request.body()
    # Use incoming content-type if present; default to FHIR JSON
    orig_ct = request.headers.get("content-type", "application/fhir+json")
    async with httpx.AsyncClient(timeout=30.0) as client:
        r = await client.post(url, content=body, headers=_proxy_headers(orig_ct))
    if r.status_code >= 400:
        # Bubble up IRIS error body to the caller for easy debugging
        raise HTTPException(status_code=r.status_code, detail=r.text)
    return Response(content=r.content, status_code=r.status_code,
                    media_type=r.headers.get("content-type", "application/fhir+json"))

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