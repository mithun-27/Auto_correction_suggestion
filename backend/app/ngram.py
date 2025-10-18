from collections import defaultdict, Counter
import re
from typing import List

_TOKEN = re.compile(r"[A-Za-z']+")

class NGramModel:
    """
    Simple Kneser-Ney-ish backoff via counts (lightweight).
    Trains on a small bundled corpus; feel free to swap for larger text.
    """

    def __init__(self, n: int = 3):
        self.n = n
        self.unigrams = Counter()
        self.bigrams = Counter()
        self.trigrams = Counter()
        self.vocab = set()

    def _tok(self, text: str) -> List[str]:
        return [t.lower() for t in _TOKEN.findall(text)]

    def fit(self, text: str):
        tok = self._tok(text)
        self.vocab.update(tok)
        self.unigrams.update(tok)
        for i in range(len(tok) - 1):
            self.bigrams[(tok[i], tok[i + 1])] += 1
        for i in range(len(tok) - 2):
            self.trigrams[(tok[i], tok[i + 1], tok[i + 2])] += 1

    def suggest(self, context: str, top_k: int = 5) -> List[str]:
        ctx = self._tok(context)
        if not ctx:
            # most frequent words
            return [w for w, _ in self.unigrams.most_common(top_k)]

        # Try trigram (use last two words)
        if len(ctx) >= 2:
            w1, w2 = ctx[-2], ctx[-1]
            cands = [(w3, cnt) for (a, b, w3), cnt in self.trigrams.items() if a == w1 and b == w2]
            if cands:
                cands.sort(key=lambda x: x[1], reverse=True)
                return [w for w, _ in cands[:top_k]]

        # Fallback: bigram (use last one word)
        w = ctx[-1]
        cands = [(w2, cnt) for (a, w2), cnt in self.bigrams.items() if a == w]
        if cands:
            cands.sort(key=lambda x: x[1], reverse=True)
            return [w for w, _ in cands[:top_k]]

        # Fallback: unigrams
        return [w for w, _ in self.unigrams.most_common(top_k)]

# Small built-in corpus (replace/extend with your domain data)
DEFAULT_CORPUS = """
I am writing a simple sentence to test the next word suggestion model.
I am going to school and I am going to work.
This is a modern autocorrection and autosuggestion demo built with FastAPI and a tiny n-gram model.
Machine learning models can predict the next word based on previous words.
I love building AI tools for writing and productivity.
Thank you for trying this demo. Have a great day.
"""

ngram_model = NGramModel(n=3)
ngram_model.fit(DEFAULT_CORPUS)
