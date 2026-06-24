"""Shared helpers for the Fórum Brasileiro de Segurança Pública connector.

The source's flagship product is the annual *Anuário Brasileiro de Segurança
Pública*, published in the FBSP DSpace repository as one multi-sheet xlsx
"PLANILHA" workbook. Each entity in this connector is one data table (a sheet)
inside that workbook. The download stage resolves the latest edition, downloads
the workbook, and parses the requested sheet into a tidy long table.

Sheet codes (T01, T02, ...) shift between annual editions, so an entity is keyed
by a slug of its (stable) Índice title. At download time we re-parse the Índice,
slug each table title the same way collect did, and match the entity to its
current sheet — so the connector tracks the latest edition automatically.
"""

import io
import re
import unicodedata

from openpyxl import load_workbook

from subsets_utils import get, transient_retry

API = "https://publicacoes.forumseguranca.org.br/server/api"

# Brazilian geographic labels (normalized: ascii, lowercase) that mark a data row.
_UF = {
    "acre", "alagoas", "amapa", "amazonas", "bahia", "ceara", "distrito federal",
    "espirito santo", "goias", "maranhao", "mato grosso", "mato grosso do sul",
    "minas gerais", "para", "paraiba", "parana", "pernambuco", "piaui",
    "rio de janeiro", "rio grande do norte", "rio grande do sul", "rondonia",
    "roraima", "santa catarina", "sao paulo", "sergipe", "tocantins",
}
_REGIONS = {
    "regiao norte", "regiao nordeste", "regiao sudeste", "regiao sul",
    "regiao centro-oeste", "regiao centro oeste", "norte", "nordeste",
    "sudeste", "sul", "centro-oeste", "centro oeste",
}
_GEO = _UF | _REGIONS | {"brasil"}
_NULLISH = {"", "-", "--", "..", "...", "n/d", "nd", "s/i", "s/d", "x"}


def slug(s: str) -> str:
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode()
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()
    return s[:70].strip("-")


def _norm(v) -> str:
    if v is None:
        return ""
    s = unicodedata.normalize("NFKD", str(v)).encode("ascii", "ignore").decode()
    return re.sub(r"\s+", " ", s).strip().lower()


def _as_year(v):
    try:
        n = int(float(v))
    except (TypeError, ValueError):
        return None
    return n if 1995 <= n <= 2026 else None


def _as_float(v):
    if v is None:
        return None
    if isinstance(v, (int, float)):
        f = float(v)
        return f
    s = str(v).strip()
    if _norm(s) in _NULLISH:
        return None
    s = s.replace("%", "").strip()
    # Brazilian decimals occasionally arrive as text "1.234,5"
    if re.fullmatch(r"-?\d{1,3}(\.\d{3})*(,\d+)?", s):
        s = s.replace(".", "").replace(",", ".")
    else:
        s = s.replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return None


def _geo_level(norm_label: str) -> str:
    if norm_label == "brasil":
        return "brasil"
    if norm_label in _REGIONS:
        return "regiao"
    return "uf"


@transient_retry()
def _get_json(url: str):
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


@transient_retry()
def _get_bytes(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 240.0))
    resp.raise_for_status()
    return resp.content


def resolve_latest_anuario() -> dict:
    """Newest 'Anuário Brasileiro de Segurança Pública' edition that ships a
    PLANILHA xlsx, via the public DSpace discover API."""
    url = (
        API + "/discover/search/objects?query="
        "Anu%C3%A1rio%20Brasileiro%20de%20Seguran%C3%A7a%20P%C3%BAblica"
        "&dsoType=item&sort=dc.date.issued,DESC&size=40&page=0"
    )
    objs = _get_json(url)["_embedded"]["searchResult"]["_embedded"]["objects"]
    for o in objs:
        ind = o["_embedded"]["indexableObject"]
        md = ind.get("metadata", {})
        title = md.get("dc.title", [{}])[0].get("value", "")
        if "Anuário Brasileiro de Segurança Pública" not in title:
            continue
        date = md.get("dc.date.issued", [{}])[0].get("value", "")
        bundles = _get_json(f"{API}/core/items/{ind['uuid']}/bundles")
        for bn in bundles["_embedded"]["bundles"]:
            if bn["name"] != "ORIGINAL":
                continue
            bits = _get_json(f"{API}/core/bundles/{bn['uuid']}/bitstreams")
            for x in bits["_embedded"]["bitstreams"]:
                nm = x["name"].lower()
                if nm.endswith(".xlsx") and "planilha" in nm:
                    return {
                        "title": title,
                        "date": date,
                        "item_uuid": ind["uuid"],
                        "bitstream_uuid": x["uuid"],
                    }
    raise RuntimeError("no Anuário PLANILHA xlsx found via DSpace discover")


def fetch_workbook() -> bytes:
    src = resolve_latest_anuario()
    return _get_bytes(f"{API}/core/bitstreams/{src['bitstream_uuid']}/content")


def index_slug_to_code(xlsx: bytes) -> dict:
    """Map slug(table title) -> sheet code (T01, ...) from the workbook Índice,
    matching exactly how collect keyed its entities."""
    import xml.etree.ElementTree as ET

    M = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
    ns = {
        "m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
        "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    }
    rid = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"
    z = __import__("zipfile").ZipFile(io.BytesIO(xlsx))
    shared = []
    r = ET.fromstring(z.read("xl/sharedStrings.xml"))
    for si in r:
        shared.append("".join(t.text or "" for t in si.iter(M + "t")))
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    sheet_els = wb.find("m:sheets", ns)
    names = {s.get("name") for s in sheet_els}
    rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
    relmap = {x.get("Id"): x.get("Target") for x in rels}
    idx_target = next(
        relmap[s.get(rid)] for s in sheet_els if s.get("name") == "Índice"
    )

    def cell(c):
        v = c.find("m:v", ns)
        if v is None:
            return ""
        if c.get("t") == "s":
            return shared[int(v.text)]
        return v.text or ""

    ridx = ET.fromstring(z.read("xl/" + idx_target))
    out = {}
    seen = set()
    for row in ridx.iter(M + "row"):
        cells = [cell(c).strip() for c in row.findall("m:c", ns)]
        c0 = cells[0] if cells else ""
        c1 = cells[1] if len(cells) > 1 else ""
        mt = re.match(r"Tabela\s+(\d+)", c0, re.I)
        if not mt:
            continue
        code = f"T{int(mt.group(1)):02d}"
        if code not in names:
            continue
        title = c1 or code
        key = slug(title) or code.lower()
        if key in seen:
            key = f"{key}-{code.lower()}"
        seen.add(key)
        out[key] = code
    return out


def _measure_for(grid, year_row, ci, top):
    """Best label describing the metric of column `ci`, searched in the header
    band [top, year_row): nearest non-empty, non-year cell at the column, then
    leftward along each header row."""
    parts = []
    for r in range(year_row - 1, top - 1, -1):
        row = grid[r]
        val = row[ci] if ci < len(row) else None
        if val in (None, "") or _as_year(val) is not None:
            # climb left within this row for a spanning header
            val = None
            for cc in range(min(ci, len(row) - 1), -1, -1):
                cand = row[cc]
                if cand not in (None, "") and _as_year(cand) is None:
                    val = cand
                    break
        if val not in (None, ""):
            t = re.sub(r"\s+", " ", str(val)).strip()
            if t and t not in parts:
                parts.append(t)
        if len(parts) >= 2:
            break
    return " / ".join(reversed(parts)) if parts else None


def parse_table(xlsx: bytes, sheet_code: str) -> list[dict]:
    """Parse one UF-by-year cross-tab sheet into long rows.

    Output rows: geography, geo_level, year, measure, value. Handles multiple
    stacked metric blocks (each its own year-header row) and side-by-side
    metric blocks (absolutos / taxas) within one header row.
    """
    wb = load_workbook(io.BytesIO(xlsx), read_only=True, data_only=True)
    if sheet_code not in wb.sheetnames:
        raise RuntimeError(f"sheet {sheet_code} not present in workbook")
    ws = wb[sheet_code]
    grid = [list(r) for r in ws.iter_rows(values_only=True)]
    wb.close()

    blocks = []  # (year_row_index, {col: year})
    for ri, row in enumerate(grid):
        colyear = {}
        for ci, v in enumerate(row):
            y = _as_year(v)
            if y is not None:
                colyear[ci] = y
        if len(colyear) >= 3:
            blocks.append((ri, colyear))
    if not blocks:
        return []

    out = []
    for bi, (ri, colyear) in enumerate(blocks):
        top = blocks[bi - 1][0] + 1 if bi > 0 else 0
        next_ri = blocks[bi + 1][0] if bi + 1 < len(blocks) else len(grid)
        measures = {ci: _measure_for(grid, ri, ci, top) for ci in colyear}
        for r in range(ri + 1, next_ri):
            row = grid[r]
            label = next((v for v in row if v not in (None, "")), None)
            nl = _norm(label)
            if nl not in _GEO:
                continue
            for ci, year in colyear.items():
                val = _as_float(row[ci] if ci < len(row) else None)
                if val is None:
                    continue
                out.append({
                    "geography": re.sub(r"\s+", " ", str(label)).strip(),
                    "geo_level": _geo_level(nl),
                    "year": int(year),
                    "measure": measures.get(ci),
                    "value": float(val),
                })
    return out
