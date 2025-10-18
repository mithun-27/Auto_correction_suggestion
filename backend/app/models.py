from pydantic import BaseModel
from typing import List, Tuple

class CorrectRequest(BaseModel):
    text: str

class CorrectResponse(BaseModel):
    corrected_text: str
    tokens: List[Tuple[str, str]]  # (original, corrected)
    notes: str

class SuggestRequest(BaseModel):
    context: str
    top_k: int = 5

class SuggestResponse(BaseModel):
    suggestions: List[str]
    notes: str
