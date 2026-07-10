"""Duty to Serve eligibility and performance files.

FHFA publishes this product as several ZIP bundles whose members have related
but non-identical schemas. Keep the raw table sparse and provenance-rich:
all source columns are normalized to strings, with dataset_part/source_file
columns preserving the original component.
"""

from __future__ import annotations

import io
import re
import zipfile

from subsets_utils import NodeSpec

from utils import _df_to_string_parquet, _get

ELIGIBILITY_PAGE = "https://www.fhfa.gov/data/duty-to-serve/eligibility-data"
PERFORMANCE_PAGE = "https://www.fhfa.gov/data/duty-to-serve/performance-data"


def _absolute(href: str) -> str:
    return href if href.startswith("http") else f"https://www.fhfa.gov{href}"


def _zip_links(page_url: str) -> list[str]:
    page = _get(page_url).text
    links = re.findall(r'href="([^"]+\.zip)"', page, flags=re.I)
    seen = set()
    out = []
    for href in links:
        url = _absolute(href)
        if url not in seen:
            seen.add(url)
            out.append(url)
    if not out:
        raise AssertionError(f"no ZIP links found on {page_url}")
    return out


def _norm_col(col: object) -> str:
    s = str(col).replace("\ufeff", "").strip().lower()
    s = re.sub(r"[^a-z0-9]+", "_", s).strip("_")
    return s or "unnamed"


def _year_from_name(value: str) -> str | None:
    match = re.search(r"(20\d{2})", value)
    return match.group(1) if match else None


def _read_member(data: bytes, name: str):
    import pandas as pd

    lower = name.lower()
    if lower.endswith(".csv"):
        return [pd.read_csv(io.BytesIO(data), dtype=str, keep_default_na=False, na_values=[])]
    if lower.endswith(".txt"):
        return [pd.read_csv(io.BytesIO(data), sep=r"\s+", dtype=str, keep_default_na=False, na_values=[])]
    if lower.endswith((".xlsx", ".xls")):
        frames = []
        xl = pd.ExcelFile(io.BytesIO(data))
        for sheet in xl.sheet_names:
            df = pd.read_excel(xl, sheet_name=sheet, dtype=str, keep_default_na=False, na_values=[])
            df["sheet_name"] = sheet
            frames.append(df)
        return frames
    return []


def _frames_from_zip(url: str, dataset_part: str):
    import pandas as pd

    resp = _get(url)
    frames = []
    with zipfile.ZipFile(io.BytesIO(resp.content)) as zf:
        for name in zf.namelist():
            if not name.lower().endswith((".csv", ".txt", ".xlsx", ".xls")):
                continue
            for df in _read_member(zf.read(name), name):
                df = df.rename(columns={c: _norm_col(c) for c in df.columns})
                df = df.loc[:, [c for c in df.columns if c != "unnamed"]]
                df["dataset_part"] = dataset_part
                df["source_file"] = name
                df["source_url"] = url
                df["release_year"] = _year_from_name(name) or _year_from_name(url)
                frames.append(df)
    if not frames:
        raise AssertionError(f"no tabular members found in {url}")
    return frames


def fetch_duty_to_serve(node_id: str) -> None:
    import pandas as pd

    frames = []
    for url in _zip_links(ELIGIBILITY_PAGE):
        frames.extend(_frames_from_zip(url, "eligibility"))
    for url in _zip_links(PERFORMANCE_PAGE):
        frames.extend(_frames_from_zip(url, "performance"))
    combined = pd.concat(frames, ignore_index=True, sort=False)
    _df_to_string_parquet(combined, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="fhfa-duty-to-serve", fn=fetch_duty_to_serve, kind="download"),
]
