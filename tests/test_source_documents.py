"""Source documents must stay out of git and not be referenced by local path."""

import re
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
LOCAL_DOC_REF = re.compile(r"local/[^\s`'\")\]]*\.(pdf|jpe?g)", re.IGNORECASE)
EXCLUDED_PREFIXES = ("openspec/changes/archive/",)


def tracked_files() -> list[str]:
    out = subprocess.run(
        ["git", "ls-files"], cwd=PROJECT_ROOT, capture_output=True, text=True, check=True
    ).stdout
    return [f for f in out.splitlines() if not f.startswith(EXCLUDED_PREFIXES)]


def test_no_source_documents_tracked():
    tracked = [f for f in tracked_files() if f.startswith("local/")]
    assert not tracked, f"source documents are tracked in git: {tracked}"


def test_no_local_path_references():
    hits = []
    for rel in tracked_files():
        path = PROJECT_ROOT / rel
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue  # binary (STEP/STL)
        for lineno, line in enumerate(text.splitlines(), 1):
            if LOCAL_DOC_REF.search(line):
                hits.append(f"{rel}:{lineno}: {line.strip()}")
    assert not hits, "local/ source-document paths found:\n" + "\n".join(hits)


def test_local_dir_is_gitignored():
    probe = "local/" + "probe.pdf"  # split so the scan above doesn't match itself
    result = subprocess.run(["git", "check-ignore", "-q", probe], cwd=PROJECT_ROOT)
    assert result.returncode == 0, "/local/ must stay in .gitignore"
