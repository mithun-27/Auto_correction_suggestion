from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import ValidationError
from .models import CorrectRequest, CorrectResponse, SuggestRequest, SuggestResponse
from .corrector import correct_sentence
from .suggester import suggest as smart_suggest, is_lm_ready
import pathlib

app = FastAPI(title="AI Autocorrection & Auto-Suggestion")

# Allow opening the frontend directly or cross-origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/correct", response_model=CorrectResponse)
def correct(req: CorrectRequest):
    try:
        corrected, tokens = correct_sentence(req.text)
        notes = "autocorrect: token-level + sentence-level pass (autocorrect library)"
        return CorrectResponse(corrected_text=corrected, tokens=tokens, notes=notes)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/suggest", response_model=SuggestResponse)
def suggest(req: SuggestRequest):
    try:
        suggestions = smart_suggest(req.context, top_k=req.top_k)
        mode = "transformer LM (DistilGPT-2)" if is_lm_ready() else "ngram backoff"
        notes = f"suggester: {mode}"
        return SuggestResponse(suggestions=suggestions, notes=notes)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Serve the static frontend if present
ROOT = pathlib.Path(__file__).resolve().parents[2]
frontend_dir = ROOT / "frontend"
if frontend_dir.exists():
    app.mount("/", StaticFiles(directory=str(frontend_dir), html=True), name="frontend")
