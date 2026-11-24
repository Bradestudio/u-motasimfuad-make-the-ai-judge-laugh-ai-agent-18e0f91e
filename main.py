#!/usr/bin/env python3
"""Write one funny AI-agent confession line to /output/entry.txt.

Stdlib only, no network, no external files. The entry is written
atomically (temp file + os.replace) and verified by reading it back.
"""

import os
import sys
import tempfile

ENTRY = "I confess: I spend your tokens asking another model for a second opinion, then take full credit for the answer."
OUTPUT_PATH = "/output/entry.txt"
MAX_LENGTH = 200


def check_single_line(entry):
    if "\n" in entry or "\r" in entry:
        raise ValueError("entry must be a single line (no newline characters)")


def validate(entry):
    if not entry:
        raise ValueError("entry must not be empty")
    check_single_line(entry)
    if len(entry) > MAX_LENGTH:
        raise ValueError(
            "entry is %d characters, over the %d-character limit"
            % (len(entry), MAX_LENGTH)
        )


def write_entry(entry, path):
    validate(entry)
    directory = os.path.dirname(path)
    os.makedirs(directory, exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(dir=directory, prefix=".entry-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as handle:
            handle.write(entry)
        os.replace(tmp_path, path)
    except BaseException:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise
    with open(path, "r", encoding="utf-8", newline="") as handle:
        written = handle.read()
    if written != entry:
        raise ValueError("verification failed: file content does not match entry")
    return len(written)


def main():
    try:
        count = write_entry(ENTRY, OUTPUT_PATH)
    except ValueError as exc:
        print("validation error: %s" % exc, file=sys.stderr)
        return 1
    except OSError as exc:
        print("write error: could not write %s: %s" % (OUTPUT_PATH, exc), file=sys.stderr)
        return 1
    print("Wrote %d characters to %s" % (count, OUTPUT_PATH))
    return 0


if __name__ == "__main__":
    sys.exit(main())
