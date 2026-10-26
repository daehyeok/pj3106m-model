"""Verify a local copy of the source datasheet against the recorded SHA-256.

The datasheet is not stored in git. Point this command at a copy with
``--datasheet PATH`` or the ``PJ3106M_DATASHEET`` environment variable (the
option wins). The path is only used for this check and never written anywhere.

Exit codes: 0 = match, 1 = checksum mismatch, 2 = no path given / file missing.
"""

import argparse
import hashlib
import os
import sys
from pathlib import Path

from pj3106m_model import params as p

ENV_VAR = "PJ3106M_DATASHEET"
EXIT_MATCH = 0
EXIT_MISMATCH = 1
EXIT_UNAVAILABLE = 2


def sha256_of(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            digest.update(chunk)
    return digest.hexdigest()


def resolve_path(cli_value: str | None) -> Path | None:
    value = cli_value or os.environ.get(ENV_VAR)
    return Path(value).expanduser() if value else None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--datasheet",
        metavar="PATH",
        help=f"path to the datasheet PDF (default: ${ENV_VAR})",
    )
    args = parser.parse_args(argv)

    ident = (
        f"{p.DATASHEET_MODEL} rev {p.DATASHEET_REVISION} ({p.DATASHEET_DATE}), "
        f"LCSC {p.LCSC_PART}"
    )
    path = resolve_path(args.datasheet)
    if path is None:
        print(
            f"error: no datasheet path given; use --datasheet PATH or set {ENV_VAR}\n"
            f"expected: {ident}",
            file=sys.stderr,
        )
        return EXIT_UNAVAILABLE
    if not path.is_file():
        print(f"error: datasheet not found: {path}", file=sys.stderr)
        return EXIT_UNAVAILABLE

    actual = sha256_of(path)
    if actual != p.DATASHEET_SHA256:
        print(
            f"MISMATCH: {path} is not {ident}\n"
            f"  expected sha256 {p.DATASHEET_SHA256}\n"
            f"  actual   sha256 {actual}",
            file=sys.stderr,
        )
        return EXIT_MISMATCH
    print(f"OK: {path} matches {ident}")
    return EXIT_MATCH


def cli() -> None:
    sys.exit(main())


if __name__ == "__main__":
    cli()
