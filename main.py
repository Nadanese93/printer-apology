import os
import sys

ENTRY = "Sorry I ate a rainforest. You print every email 'just in case' — I'm the accomplice, you're the mastermind."

EXPECTED_LEN = 107
EXPECTED_SHA256 = "4311b40c0402d005d893b50af616b8c887f535a01a33093496a398300dd06635"


def verify(path):
    """Read entry.txt back from disk and verify it is byte-identical to ENTRY.

    Checks: valid UTF-8, length within 1-120, no trailing newline,
    and exact byte equality against the canonical entry.
    Returns 0 on success, 1 on any failure.
    """
    import hashlib

    try:
        with open(path, "rb") as f:
            data = f.read()
    except OSError as exc:
        print(f"verify: cannot read {path}: {exc}", file=sys.stderr)
        return 1
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        print(f"verify: not valid UTF-8: {exc}", file=sys.stderr)
        return 1
    if not (1 <= len(text) <= 120):
        print(f"verify: length {len(text)} outside 1-120", file=sys.stderr)
        return 1
    if text.endswith("\n"):
        print("verify: trailing newline present", file=sys.stderr)
        return 1
    if hashlib.sha256(data).hexdigest() != EXPECTED_SHA256:
        print("verify: sha256 mismatch", file=sys.stderr)
        return 1
    if text != ENTRY:
        print("verify: content differs from ENTRY", file=sys.stderr)
        return 1
    return 0


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "wb") as f:
        f.write(ENTRY.encode("utf-8"))
    return verify(path)


if __name__ == "__main__":
    sys.exit(main())
