"""Shared helpers for the ARCEP connector.

`family_slug_of` reproduces the schema-family grouping the collect stage used:
within one data.gouv.fr dataset, resources that are time/geo partitions of the
same schema (one CSV per quarter, one per day) collapse to a single family, so
a single download node concatenates the whole historical series. `decode_bytes`
and `parse_csv` handle the ARCEP CSV quirks (cp1252 encoding, ';' delimiter,
occasional preamble lines, accented headers).
"""

import csv
import io
import re

_ACCENTS = (
    ("àâä", "a"), ("éèêë", "e"), ("îï", "i"), ("ôö", "o"),
    ("ùûü", "u"), ("ç", "c"), ("’'", ""),
)


def _deaccent(text: str) -> str:
    for group, repl in _ACCENTS:
        for ch in group:
            text = text.replace(ch, repl)
    return text


def slugify(text: str) -> str:
    text = _deaccent(text.lower())
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return re.sub(r"-+", "-", text)


def _family_key(title: str) -> str:
    """Normalize a resource title to its schema-family key by stripping
    time-partition tokens (mirrors collect's grouping exactly)."""
    t = (title or "").strip()
    t = re.sub(r"\.(csv|xlsx|xls|json|geojson|zip|7z|txt|pdf)\s*$", "", t, flags=re.I)
    t = re.sub(r"^\s*\d{4}\s*[-_ ]?\s*t\s*\d\s*[-_ :]*", "", t, flags=re.I)
    t = re.sub(r"^\s*\d{4}-\d{2}-\d{2}\s*[-_ :]*", "", t)
    t = re.sub(r"^\s*\d{4}[ _-]\d{2}[ _-]+", "", t)
    t = re.sub(r"^\s*\d{4}\s+", "", t)
    t = re.sub(r"[ _-]t\d[ _-]\d{4}", "", t, flags=re.I)
    t = re.sub(r"\s*\(?\s*\d{4}\s*[-–/]\s*\d{4}\)?\s*$", "", t)
    t = re.sub(r"\s*\(?\s*\d{1,2}/\d{4}\s*[-–].*$", "", t)
    t = re.sub(r"\s+\d{4}\s*$", "", t)
    t = t.strip(" -–_:()")
    t = re.sub(r"deploiements\b", "deploiement", t, flags=re.I)
    return t


def family_slug_of(title: str, dataset_slug: str) -> str:
    """The family-slug a resource belongs to. Empty family keys fall back to the
    dataset slug (matches collect's behaviour for date-only titles)."""
    return slugify(_family_key(title)) or dataset_slug or "data"


def period_from_title(title: str) -> str | None:
    """Best-effort partition coordinate extracted from a resource title.

    Prefer the latest endpoint of a title range such as
    ``11/2022 - 09/2025``; that is the resource vintage useful for freshness.
    Then fall back to YYYYTX / YYYY_TX quarter, YYYY-MM-DD day, or a bare year.
    """
    t = title or ""
    month_years = re.findall(r"(?<!\d)(\d{1,2})/(\d{4})(?!\d)", t)
    if month_years:
        month, year = month_years[-1]
        return f"{year}-{int(month):02d}"
    m = re.search(r"(?<!\d)(\d{4})[ _-]?[Tt](\d)(?!\d)", t)
    if m:
        return f"{m.group(1)}-T{m.group(2)}"
    m = re.search(r"\b(\d{4}-\d{2}-\d{2})\b", t)
    if m:
        return m.group(1)
    m = re.search(r"\b(19|20)\d{2}\b", t)
    if m:
        return m.group(0)
    return None


def decode_bytes(content: bytes) -> str:
    """ARCEP CSVs are usually cp1252; a few are UTF-8. Try UTF-8 (with BOM)
    first, fall back to cp1252 which never raises on byte input."""
    for enc in ("utf-8-sig", "utf-8", "cp1252"):
        try:
            return content.decode(enc)
        except UnicodeDecodeError:
            continue
    return content.decode("cp1252", errors="replace")


def _sanitize_columns(header: list[str]) -> list[str]:
    out: list[str] = []
    seen: dict[str, int] = {}
    for i, raw in enumerate(header):
        name = re.sub(r"_+", "_", re.sub(r"[^a-z0-9]+", "_", _deaccent((raw or "").lower()))).strip("_")
        if not name:
            name = f"col_{i}"
        if name in seen:
            seen[name] += 1
            name = f"{name}_{seen[name]}"
        else:
            seen[name] = 0
        out.append(name)
    return out


def _pick_delimiter(lines: list[str]) -> str:
    sample = "\n".join(lines[:20])
    return ";" if sample.count(";") >= sample.count(",") else ","


def _header_index(rows: list[list[str]]) -> int:
    """Skip any preamble lines (e.g. 'Source: ...;;;;') — the header is the
    first row where most fields are non-empty and there are >= 2 of them."""
    for i, row in enumerate(rows[:10]):
        non_empty = sum(1 for c in row if (c or "").strip())
        if len(row) >= 2 and non_empty >= max(2, 0.5 * len(row)):
            return i
    return 0


def parse_csv(text: str) -> list[dict]:
    """Parse ARCEP CSV text into a list of all-string dicts. Delimiter and a
    leading preamble row are auto-detected; values are kept as strings to
    preserve the source faithfully (decimal commas, NA sentinels, leading
    zeros on codes)."""
    lines = [ln for ln in text.splitlines() if ln.strip() != ""]
    if not lines:
        return []
    delim = _pick_delimiter(lines)
    rows = list(csv.reader(io.StringIO("\n".join(lines)), delimiter=delim))
    if not rows:
        return []
    h = _header_index(rows)
    header = _sanitize_columns(rows[h])
    out: list[dict] = []
    width = len(header)
    for row in rows[h + 1:]:
        if not any((c or "").strip() for c in row):
            continue
        rec = {header[i]: (row[i] if i < len(row) else None) for i in range(width)}
        out.append(rec)
    return out
