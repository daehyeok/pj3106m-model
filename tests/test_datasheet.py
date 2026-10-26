"""Tests for the datasheet verification command (no real datasheet needed)."""

import hashlib

import pytest

from pj3106m_model import datasheet, params


@pytest.fixture
def fake_pdf(tmp_path, monkeypatch):
    """A temp file whose SHA-256 is patched in as the expected datasheet hash."""
    path = tmp_path / "datasheet.pdf"
    path.write_bytes(b"%PDF-1.4 fake datasheet\n")
    monkeypatch.setattr(
        params, "DATASHEET_SHA256", hashlib.sha256(path.read_bytes()).hexdigest()
    )
    return path


@pytest.fixture(autouse=True)
def no_env(monkeypatch):
    monkeypatch.delenv(datasheet.ENV_VAR, raising=False)


def test_match_via_option(fake_pdf, capsys):
    assert datasheet.main(["--datasheet", str(fake_pdf)]) == 0
    assert "OK" in capsys.readouterr().out


def test_match_via_env(fake_pdf, monkeypatch):
    monkeypatch.setenv(datasheet.ENV_VAR, str(fake_pdf))
    assert datasheet.main([]) == 0


def test_option_overrides_env(fake_pdf, tmp_path, monkeypatch):
    monkeypatch.setenv(datasheet.ENV_VAR, str(tmp_path / "missing.pdf"))
    assert datasheet.main(["--datasheet", str(fake_pdf)]) == 0


def test_mismatch_prints_both_hashes(fake_pdf, tmp_path, capsys):
    other = tmp_path / "other.pdf"
    other.write_bytes(b"a different revision\n")
    assert datasheet.main(["--datasheet", str(other)]) == 1
    err = capsys.readouterr().err
    assert "MISMATCH" in err
    assert params.DATASHEET_SHA256 in err
    assert hashlib.sha256(other.read_bytes()).hexdigest() in err


def test_missing_file(tmp_path, capsys):
    assert datasheet.main(["--datasheet", str(tmp_path / "nope.pdf")]) == 2
    assert "not found" in capsys.readouterr().err


def test_no_path_given(capsys):
    assert datasheet.main([]) == 2
    err = capsys.readouterr().err
    assert datasheet.ENV_VAR in err and "--datasheet" in err


def test_recorded_identity_is_pj3106m_rev_a():
    assert params.DATASHEET_MODEL == "PJ-3106M (YBC01)"
    assert params.DATASHEET_REVISION == "A"
    assert params.DATASHEET_SHA256 == (
        "88db1b26c288bbaa0537e7a184d20efc260de7c7e152d95f0d4d86067e96ea4f"
    )
    assert params.LCSC_PART == "C7428681"
    assert len(params.DATASHEET_SHA256) == 64
