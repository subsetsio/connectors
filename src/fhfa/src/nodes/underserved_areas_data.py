"""Underserved Areas data.

FHFA publishes one annual ZIP with a fixed-width text file plus PDFs. Fetch all
listed annual text files into one sparse all-string Parquet table.
"""

from __future__ import annotations

import io
import re
import zipfile

from subsets_utils import NodeSpec

from utils import _df_to_string_parquet, _get

UNDERSERVED_PAGE = "https://www.fhfa.gov/data/underserved-areas"


def _absolute(href: str) -> str:
    return href if href.startswith("http") else f"https://www.fhfa.gov{href}"


def _zip_links() -> list[str]:
    page = _get(UNDERSERVED_PAGE).text
    links = re.findall(r'href="([^"]+\.zip)"', page, flags=re.I)
    out = []
    seen = set()
    for href in links:
        url = _absolute(href)
        if url not in seen:
            seen.add(url)
            out.append(url)
    if not out:
        raise AssertionError("no underserved-area ZIP links found")
    return out


def _year_from_name(value: str) -> str | None:
    match = re.search(r"(20\d{2})", value)
    return match.group(1) if match else None


def _norm_col(col: object) -> str:
    s = str(col).replace("\ufeff", "").strip().lower()
    s = re.sub(r"[^a-z0-9]+", "_", s).strip("_")
    return s or "unnamed"


def fetch_underserved_areas_data(node_id: str) -> None:
    import pandas as pd

    frames = []
    for url in _zip_links():
        resp = _get(url)
        with zipfile.ZipFile(io.BytesIO(resp.content)) as zf:
            for name in zf.namelist():
                if not name.lower().endswith(".txt"):
                    continue
                df = pd.read_csv(
                    io.BytesIO(zf.read(name)),
                    sep=r"\s+",
                    dtype=str,
                    keep_default_na=False,
                    na_values=[],
                    engine="python",
                    on_bad_lines="skip",
                )
                df = df.rename(columns={c: _norm_col(c) for c in df.columns})
                df["release_year"] = _year_from_name(name) or _year_from_name(url)
                df["source_file"] = name
                df["source_url"] = url
                frames.append(df)
    if not frames:
        raise AssertionError("no underserved-area text members found")
    combined = pd.concat(frames, ignore_index=True, sort=False)
    _df_to_string_parquet(combined, node_id)


DOWNLOAD_SPECS = []
