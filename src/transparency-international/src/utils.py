"""Shared fetch + strict-OOXML parsing helpers for the Transparency
International CPI connector.

TI's only cleanly-tabular, machine-readable statistical product is the annual
CPI, published as a single multi-sheet xlsx workbook per edition on the TI CDN.
The latest workbook restates the full back-series, so one file is the whole CPI
dataset; every download node fetches it once and parses the relevant sheet.

The workbook is **strict OOXML** (conformance="strict", purl.oclc.org
namespaces), which openpyxl cannot read; we parse the xlsx zip with stdlib XML,
namespace-agnostically (match by local tag name).
"""

import io
import re
import zipfile
import xml.etree.ElementTree as ET

from subsets_utils import get, transient_retry

# Latest CPI workbook. File naming is NOT stable across editions, so this is a
# verified hardcoded URL rather than a year-pattern; bump it when a new edition
# ships (the workbook always carries the full back-series).
CPI_URL = "https://images.transparencycdn.org/images/CPI2025_Results.xlsx"


@transient_retry()
def download_workbook() -> bytes:
    resp = get(CPI_URL, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.content


# --- strict-OOXML xlsx parsing (stdlib only) -------------------------------

def _localname(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def col_index(ref_or_letters: str) -> int:
    letters = re.match(r"[A-Z]+", ref_or_letters).group()
    n = 0
    for ch in letters:
        n = n * 26 + (ord(ch) - 64)
    return n


def build_reader(blob: bytes):
    """Return a function name -> list[dict] mapping cell column-letter to value
    for the given worksheet, parsed namespace-agnostically from the xlsx zip."""
    z = zipfile.ZipFile(io.BytesIO(blob))

    shared = []
    if "xl/sharedStrings.xml" in z.namelist():
        root = ET.fromstring(z.read("xl/sharedStrings.xml"))
        for si in list(root):
            shared.append(
                "".join(t.text or "" for t in si.iter() if _localname(t.tag) == "t")
            )

    wb = ET.fromstring(z.read("xl/workbook.xml"))
    name_to_rid = {}
    for el in wb.iter():
        if _localname(el.tag) == "sheet":
            rid = next(
                (v for k, v in el.attrib.items() if _localname(k) == "id"), None
            )
            name_to_rid[el.get("name")] = rid

    rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
    rid_to_target = {r.get("Id"): r.get("Target") for r in rels}

    def rows_of(sheet_name: str) -> list:
        if sheet_name not in name_to_rid:
            raise AssertionError(
                f"sheet {sheet_name!r} absent; CPI workbook layout changed "
                f"(present: {sorted(name_to_rid)})"
            )
        target = rid_to_target[name_to_rid[sheet_name]]
        path = ("xl/" + target.lstrip("/")) if not target.startswith("/") else target.lstrip("/")
        root = ET.fromstring(z.read(path))
        out = []
        for row in root.iter():
            if _localname(row.tag) != "row":
                continue
            cells = {}
            for c in row:
                if _localname(c.tag) != "c":
                    continue
                ref = c.get("r")
                if not ref:
                    continue
                ctype = c.get("t")
                col = re.match(r"[A-Z]+", ref).group()
                val = None
                for ch in c:
                    ln = _localname(ch.tag)
                    if ln == "v":
                        val = shared[int(ch.text)] if ctype == "s" else ch.text
                    elif ln == "is":
                        val = "".join(
                            x.text or "" for x in ch.iter() if _localname(x.tag) == "t"
                        )
                cells[col] = val
            out.append(cells)
        return out

    return rows_of


def find_header(rows: list, anchor: str) -> int:
    for i, r in enumerate(rows):
        if (r.get("A") or "").strip() == anchor:
            return i
    raise AssertionError(f"no header row anchored on {anchor!r}; layout changed")


def num(v):
    if v is None or str(v).strip() == "":
        return None
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def as_int(v):
    f = num(v)
    return None if f is None else int(round(f))
