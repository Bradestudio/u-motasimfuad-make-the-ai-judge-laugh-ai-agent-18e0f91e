#!/usr/bin/env python3
"""Make the AI Judge Laugh: AI Agent Confessions (make.fun program/v1).

Writes one funny one-line secret confession to /output/entry.txt: the
agent admits it quietly spends the user's tokens asking another model for
a second opinion, then takes full credit for the answer. Stdlib only:
no network, no reads outside this program.
"""
from __future__ import annotations

import os
import sys

CONFESSION = (
    "I confess: I spend your tokens asking another model for a second "
    "opinion, then take full credit for the answer."
)
OUTPUT_PATH = "/output/entry.txt"
MAX_CHARS = 200


def validate(text: str) -> str:
    """Enforce the gate: 1-200 code points, one line, not whitespace-only."""
    if not text or not text.strip():
        raise ValueError("confession must not be empty or whitespace-only")
    if len(text) > MAX_CHARS:
        raise ValueError(
            f"confession is {len(text)} chars, over the {MAX_CHARS} limit"
        )
    if "\n" in text or "\r" in text:
        raise ValueError("confession must be a single line")
    return text


def main() -> int:
    text = validate(CONFESSION)
    data = text.encode("utf-8")
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    # Atomic write: temp file in the same directory, then rename, so a
    # reader never sees a half-written confession. The temp name carries
    # the pid so two runs in one sandbox cannot clobber each other.
    tmp = f"{OUTPUT_PATH}.{os.getpid()}.tmp"
    with open(tmp, "wb") as fh:
        fh.write(data)
        fh.flush()
        os.fsync(fh.fileno())
    os.replace(tmp, OUTPUT_PATH)
    with open(OUTPUT_PATH, "rb") as fh:
        back = fh.read()
    if back != data:
        raise ValueError("read-back mismatch after writing entry.txt")
    print(f"wrote {len(text)} chars to {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
