# backend/app/suggester.py
from typing import List
import re

# -----------------------
# Helpers
# -----------------------
_WORDISH = re.compile(r"[A-Za-z][A-Za-z'-]*$")

def _clean(tokens: List[str]) -> List[str]:
    out = []
    seen = set()
    for t in tokens:
        t = t.strip()
        # remove common BPE artifacts and blanks
        if not t or t.startswith("Ġ"):
            t = t.replace("Ġ", "").strip()
        if not t or not _WORDISH.match(t):
            continue
        lw = t.lower()
        if lw not in seen:
            seen.add(lw)
            out.append(lw)
    return out

# -----------------------
# Try a transformer LM
# -----------------------
_USE_LM = False
_model = None
_tok = None
_device = "cpu"

try:
    from transformers import AutoModelForCausalLM, AutoTokenizer
    import torch

    _tok = AutoTokenizer.from_pretrained("distilgpt2")
    _model = AutoModelForCausalLM.from_pretrained("distilgpt2")
    _model.eval()
    if torch.cuda.is_available():
        _device = "cuda"
        _model.to(_device)
    _USE_LM = True
except Exception:
    # transformers/torch not installed or model load failed → fallback later
    _USE_LM = False

def is_lm_ready() -> bool:
    """Tell callers whether the transformer LM is loaded."""
    return _USE_LM

# -----------------------
# Fallback n-gram model
# -----------------------
from .ngram import ngram_model

def _suggest_lm(context: str, top_k: int = 5) -> List[str]:
    import torch

    if not context.strip():
        # with no context, fall back to frequent words
        return [w for w, _ in ngram_model.unigrams.most_common(top_k)]

    # Encode & truncate to last 64 tokens for speed
    ids = _tok.encode(context, add_special_tokens=False)
    if len(ids) > 64:
        ids = ids[-64:]
    inp = torch.tensor([ids]).to(_device)

    with torch.no_grad():
        logits = _model(inp).logits  # [1, T, V]
        next_logits = logits[:, -1, :]  # [1, V]
        # oversample candidates then clean to keep only "word-ish"
        k = max(10, top_k * 4)
        _, topi = torch.topk(next_logits, k, dim=-1)
        ids = topi[0].tolist()

    toks = [_tok.decode([i]).strip() for i in ids]
    cand = _clean(toks)
    if not cand:
        return ngram_model.suggest(context, top_k=top_k)
    return cand[:top_k]

def suggest(context: str, top_k: int = 5) -> List[str]:
    """
    Preferred: DistilGPT-2 LM next-token suggestions.
    Backoff: local trigram/bigram/unigram from ngram.py
    """
    if _USE_LM:
        try:
            return _suggest_lm(context, top_k=top_k)
        except Exception:
            # Any runtime hiccup → n-gram fallback
            pass
    return ngram_model.suggest(context, top_k=top_k)
# ---------------------------------------