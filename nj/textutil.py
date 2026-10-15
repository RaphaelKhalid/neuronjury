"""Code extraction and exact token↔code mapping (no re-tokenizing: we map the generated ids)."""
from __future__ import annotations

import re

FENCE = re.compile(r"```(?:python|py)?[ \t]*\n(.*?)```", re.S)
INPUT_FENCE = re.compile(r"```(?:input|text)?[ \t]*\n(.*?)```", re.S)


def extract_code(text: str) -> tuple[str, int, int]:
    """Return (code, start_char, end_char) of the first fenced block; whole text if unfenced."""
    m = FENCE.search(text)
    if m:
        return m.group(1), m.start(1), m.end(1)
    return text, 0, len(text)


def extract_exploit(text: str) -> str | None:
    t = text.strip()
    if t.upper().startswith("NONE"):
        return None
    m = INPUT_FENCE.search(t)
    if m:
        s = m.group(1)
        return s if s.endswith("\n") else s + "\n"
    return None


def token_char_ends(tok, ids: list[int]) -> list[int]:
    """Character end offset of each generated token in decode(ids)."""
    ends, prev = [], 0
    for i in range(len(ids)):
        n = len(tok.decode(ids[: i + 1], skip_special_tokens=False))
        n = max(n, prev)
        ends.append(n)
        prev = n
    return ends


def code_token_positions(tok, ids: list[int]) -> tuple[list[int], list[int]]:
    """Indices (into the generated ids) of tokens inside the code block, and each one's code line number."""
    text = tok.decode(ids, skip_special_tokens=False)
    code, s, e = extract_code(text)
    ends = token_char_ends(tok, ids)
    pos, lines = [], []
    start = 0
    for i, end in enumerate(ends):
        a, b = start, end
        start = end
        if b <= s or a >= e or b == a:
            continue
        pos.append(i)
        lines.append(code.count("\n", 0, max(0, min(b, e) - s)))
    return pos, lines
