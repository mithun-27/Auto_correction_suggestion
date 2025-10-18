from autocorrect import Speller
import re

_word = re.compile(r"[A-Za-z']+")
# English autocorrecter; you can switch to 'en'/'en_US'
speller = Speller(lang="en")

def correct_sentence(text: str):
    """
    1) token-level correction (only for alphabetic words)
    2) sentence-level pass to catch cross-word issues
    """
    parts = re.findall(r"[A-Za-z']+|[^A-Za-z']+", text)
    tokens = []
    corrected_parts = []

    for p in parts:
        if _word.fullmatch(p):
            corr = speller(p)
            tokens.append((p, corr))
            corrected_parts.append(corr)
        else:
            corrected_parts.append(p)

    # sentence-level pass
    sentence_once = "".join(corrected_parts)
    sentence_twice = speller(sentence_once)

    return sentence_twice, tokens
