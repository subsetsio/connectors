"""DANE (Colombia) connector — SIPSA price & supply time-series.

Source: DANE's ANDA microdata catalog (NADA install) at
microdatos.dane.gov.co. The machine-readable surface is a per-study ZIP of
anonymized microdata. This connector publishes the two cleanly-structured,
recurring SIPSA series:

  * SIPSA-P  — wholesale food prices (precios mayoristas), COP/kg by product x market.
  * SIPSA-A  — food supply (abastecimiento), kg delivered by city/department x product.

Fetch shape: stateless full re-pull. Each study's ZIPs are small-to-moderate
and re-fetched in full every run (no incremental filter exists on the source —
see research download_handoff). The per-study download `resource_id`s are not
exposed by the JSON API; they are scraped from the study's get-microdata HTML
page (`mostrarModal('<file>','.../download/<resource_id>')`). The reCAPTCHA on
that page is not enforced on the direct download GET.

Schema drift is handled here in Python: column names vary across years/releases
(e.g. SIPSA-P uses `Fuente` then `Mercado`; dates are `D/MM/YYYY` or Spanish
`mmm-yy`), so each file is normalized to a canonical schema before the parquet
write. The SQL transforms stay thin (type + light aggregation).
"""

import io
import re
import zipfile
from datetime import date

import pyarrow as pa
import pyarrow.parquet as pq

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    transient_retry,
    raw_parquet_writer,
)
from constants import CATALOG_NUMERIC_ID

CATALOG_BASE = "https://microdatos.dane.gov.co/index.php/catalog"

_SPANISH_MONTHS = {
    "ene": 1, "feb": 2, "mar": 3, "abr": 4, "may": 5, "jun": 6,
    "jul": 7, "ago": 8, "sep": 9, "set": 9, "oct": 10, "nov": 11, "dic": 12,
}

_MODAL_RE = re.compile(
    r"mostrarModal\('([^']+)'\s*,\s*'([^']+/download/(\d+))\s*'\)"
)


# --------------------------------------------------------------------------- #
# Shared source access
# --------------------------------------------------------------------------- #
@transient_retry()
def _get(url: str):
    resp = get(url, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp


def _study_download_urls(numeric_id: str) -> list[tuple[str, str]]:
    """Scrape the study's get-microdata page for (filename, download_url) pairs.

    The resource ids are per-release and only live in the page HTML; dedup by
    resource id (each modal is rendered twice on the page)."""
    page = _get(f"{CATALOG_BASE}/{numeric_id}/get-microdata").text
    seen: dict[str, tuple[str, str]] = {}
    for fname, url, rid in _MODAL_RE.findall(page):
        seen[rid] = (fname.strip(), url.strip())
    files = list(seen.values())
    if not files:
        raise AssertionError(
            f"no download links scraped from study {numeric_id} get-microdata page "
            f"(page layout changed?)"
        )
    return files


def _decode(raw: bytes) -> str:
    """Decode a CSV member. Encoding varies across releases: newer files are
    UTF-8 (with BOM), older ones are cp1252/latin-1. Try strict UTF-8 first
    (fails fast on cp1252 high bytes), fall back to cp1252."""
    try:
        return raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        return raw.decode("cp1252", errors="replace")


def _csv_members(zip_bytes: bytes):
    """Yield (member_name, decoded_text) for every flat .csv in the ZIP.

    SIPSA-P / SIPSA-A ZIPs hold one CSV (plus redundant .dta/.sav of the same
    data, which we ignore)."""
    zf = zipfile.ZipFile(io.BytesIO(zip_bytes))
    for name in zf.namelist():
        if name.lower().endswith(".csv"):
            yield name, _decode(zf.read(name))


def _split_rows(text: str):
    """Yield (header_cells, row_cells_iter) for a semicolon-delimited CSV."""
    lines = text.splitlines()
    if not lines:
        return None, iter(())
    header = [h.strip().lstrip("﻿") for h in lines[0].split(";")]
    rows = (ln.split(";") for ln in lines[1:] if ln.strip())
    return header, rows


def _col_index(header: list[str], *aliases: str):
    """First header position whose normalized text matches any alias (substring)."""
    norm = [h.strip().lower() for h in header]
    for alias in aliases:
        a = alias.strip().lower()
        for i, h in enumerate(norm):
            if h == a:
                return i
        for i, h in enumerate(norm):
            if a in h:
                return i
    return None


def _parse_date(s: str):
    """Parse 'D/MM/YYYY', 'DD/MM/YYYY' or Spanish 'mmm-yy' to a date (1st of month)."""
    s = s.strip()
    if not s:
        return None
    if "/" in s:
        parts = s.split("/")
        if len(parts) == 3:
            try:
                d, m, y = int(parts[0]), int(parts[1]), int(parts[2])
                if y < 100:
                    y += 2000
                return date(y, m, d)
            except ValueError:
                return None
        return None
    # Spanish 'mmm-yy' / 'mmm-yyyy'
    m = re.match(r"([a-záéíóú]+)[-/ ]+(\d{2,4})", s.lower())
    if m and m.group(1)[:3] in _SPANISH_MONTHS:
        mon = _SPANISH_MONTHS[m.group(1)[:3]]
        y = int(m.group(2))
        if y < 100:
            y += 2000
        return date(y, mon, 1)
    return None


def _parse_number(s):
    """Colombian-locale number: '.' thousands, ',' decimal. '1.387' -> 1387.0."""
    if s is None:
        return None
    s = s.strip().strip("'").replace(" ", "")
    if not s:
        return None
    s = s.replace(".", "").replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return None


def _clean_code(s):
    if s is None:
        return None
    s = s.strip().strip("'").strip()
    return s or None


def _clean_text(s):
    if s is None:
        return None
    s = s.strip()
    return s or None


# --------------------------------------------------------------------------- #
# SIPSA-P — wholesale food prices
# --------------------------------------------------------------------------- #
_PRECIOS_SCHEMA = pa.schema([
    ("fecha", pa.date32()),
    ("grupo", pa.string()),
    ("producto", pa.string()),
    ("mercado", pa.string()),
    ("codigo_cpc", pa.string()),
    ("precio_cop_kg", pa.float64()),
    ("source_file", pa.string()),
])


def fetch_sipsa_precios(node_id: str) -> None:
    asset = node_id
    numeric_id = CATALOG_NUMERIC_ID["DANE-DIMPE-SIPSA-P-2013-2024"]
    urls = _study_download_urls(numeric_id)

    total = 0
    with raw_parquet_writer(asset, _PRECIOS_SCHEMA) as writer:
        for fname, url in urls:
            content = _get(url).content
            for member, text in _csv_members(content):
                header, rows = _split_rows(text)
                if not header:
                    continue
                i_fecha = _col_index(header, "fecha")
                i_grupo = _col_index(header, "grupo")
                i_prod = _col_index(header, "producto")
                i_merc = _col_index(header, "mercado", "fuente")
                i_cpc = _col_index(header, "codigo_cpc_ac", "codigo cpc", "cpc")
                i_precio = _col_index(header, "precio promedio por kilogramo", "precio")
                cols = {k: [] for k in
                        ("fecha", "grupo", "producto", "mercado", "codigo_cpc", "precio_cop_kg")}
                src = f"{fname}/{member}"
                for r in rows:
                    def g(idx):
                        return r[idx] if (idx is not None and idx < len(r)) else None
                    cols["fecha"].append(_parse_date(g(i_fecha) or ""))
                    cols["grupo"].append(_clean_text(g(i_grupo)))
                    cols["producto"].append(_clean_text(g(i_prod)))
                    cols["mercado"].append(_clean_text(g(i_merc)))
                    cols["codigo_cpc"].append(_clean_code(g(i_cpc)))
                    cols["precio_cop_kg"].append(_parse_number(g(i_precio)))
                if not cols["fecha"]:
                    continue
                tbl = pa.table(
                    {
                        "fecha": pa.array(cols["fecha"], pa.date32()),
                        "grupo": pa.array(cols["grupo"], pa.string()),
                        "producto": pa.array(cols["producto"], pa.string()),
                        "mercado": pa.array(cols["mercado"], pa.string()),
                        "codigo_cpc": pa.array(cols["codigo_cpc"], pa.string()),
                        "precio_cop_kg": pa.array(cols["precio_cop_kg"], pa.float64()),
                        "source_file": pa.array([src] * len(cols["fecha"]), pa.string()),
                    },
                    schema=_PRECIOS_SCHEMA,
                )
                writer.write_table(tbl)
                total += tbl.num_rows
    print(f"  {asset}: wrote {total} price rows from {len(urls)} file(s)")
    if total == 0:
        raise AssertionError(f"{asset}: parsed 0 price rows")


# --------------------------------------------------------------------------- #
# SIPSA-A — food supply / abastecimiento
# --------------------------------------------------------------------------- #
_ABAST_SCHEMA = pa.schema([
    ("fecha", pa.date32()),
    ("mercado", pa.string()),
    ("depto_codigo", pa.string()),
    ("municipio_codigo", pa.string()),
    ("departamento", pa.string()),
    ("municipio", pa.string()),
    ("grupo", pa.string()),
    ("alimento", pa.string()),
    ("cantidad_kg", pa.float64()),
    ("source_file", pa.string()),
])


def fetch_sipsa_abastecimiento(node_id: str) -> None:
    asset = node_id
    numeric_id = CATALOG_NUMERIC_ID["DANE-DIMPE-SIPSA-A-2018-2025"]
    urls = _study_download_urls(numeric_id)

    total = 0
    with raw_parquet_writer(asset, _ABAST_SCHEMA) as writer:
        for fname, url in urls:
            content = _get(url).content
            for member, text in _csv_members(content):
                header, rows = _split_rows(text)
                if not header:
                    continue
                i_fecha = _col_index(header, "fechaencuesta", "fecha")
                i_merc = _col_index(header, "fuente")
                i_dcod = _col_index(header, "cod. depto proc", "divipola depto proc", "depto")
                i_mcod = _col_index(header, "cod. municipio proc", "divipola municipio")
                i_dep = _col_index(header, "departamento proc", "departamento")
                i_mun = _col_index(header, "municipio proc", "municipio de colombia", "municipio")
                i_grupo = _col_index(header, "grupo")
                i_ali = _col_index(header, "ali")
                i_cant = _col_index(header, "cant kg", "cantidad")
                cols = {k: [] for k in
                        ("fecha", "mercado", "depto_codigo", "municipio_codigo",
                         "departamento", "municipio", "grupo", "alimento", "cantidad_kg")}
                src = f"{fname}/{member}"
                for r in rows:
                    def g(idx):
                        return r[idx] if (idx is not None and idx < len(r)) else None
                    cols["fecha"].append(_parse_date(g(i_fecha) or ""))
                    cols["mercado"].append(_clean_text(g(i_merc)))
                    cols["depto_codigo"].append(_clean_code(g(i_dcod)))
                    cols["municipio_codigo"].append(_clean_code(g(i_mcod)))
                    cols["departamento"].append(_clean_text(g(i_dep)))
                    cols["municipio"].append(_clean_text(g(i_mun)))
                    cols["grupo"].append(_clean_text(g(i_grupo)))
                    cols["alimento"].append(_clean_text(g(i_ali)))
                    cols["cantidad_kg"].append(_parse_number(g(i_cant)))
                if not cols["fecha"]:
                    continue
                tbl = pa.table(
                    {
                        "fecha": pa.array(cols["fecha"], pa.date32()),
                        "mercado": pa.array(cols["mercado"], pa.string()),
                        "depto_codigo": pa.array(cols["depto_codigo"], pa.string()),
                        "municipio_codigo": pa.array(cols["municipio_codigo"], pa.string()),
                        "departamento": pa.array(cols["departamento"], pa.string()),
                        "municipio": pa.array(cols["municipio"], pa.string()),
                        "grupo": pa.array(cols["grupo"], pa.string()),
                        "alimento": pa.array(cols["alimento"], pa.string()),
                        "cantidad_kg": pa.array(cols["cantidad_kg"], pa.float64()),
                        "source_file": pa.array([src] * len(cols["fecha"]), pa.string()),
                    },
                    schema=_ABAST_SCHEMA,
                )
                writer.write_table(tbl)
                total += tbl.num_rows
    print(f"  {asset}: wrote {total} supply rows from {len(urls)} file(s)")
    if total == 0:
        raise AssertionError(f"{asset}: parsed 0 supply rows")


# --------------------------------------------------------------------------- #
# Specs
# --------------------------------------------------------------------------- #
PRECIOS_ID = "dane-dane-dimpe-sipsa-p-2013-2024"
ABAST_ID = "dane-dane-dimpe-sipsa-a-2018-2025"

DOWNLOAD_SPECS = [
    NodeSpec(id=PRECIOS_ID, fn=fetch_sipsa_precios, kind="download"),
    NodeSpec(id=ABAST_ID, fn=fetch_sipsa_abastecimiento, kind="download"),
]

TRANSFORM_SPECS = [
    # Prices: faithful monthly/daily wholesale price observations, deduped.
    SqlNodeSpec(
        id=f"{PRECIOS_ID}-transform",
        deps=[PRECIOS_ID],
        sql=f'''
            SELECT DISTINCT
                fecha,
                grupo,
                producto,
                mercado,
                codigo_cpc,
                precio_cop_kg
            FROM "{PRECIOS_ID}"
            WHERE fecha IS NOT NULL
              AND producto IS NOT NULL
              AND precio_cop_kg IS NOT NULL
              AND precio_cop_kg > 0
        ''',
    ),
    # Supply: aggregate record-level deliveries to monthly kg by
    # department x group x food item (compact, analysis-ready supply series).
    SqlNodeSpec(
        id=f"{ABAST_ID}-transform",
        deps=[ABAST_ID],
        sql=f'''
            SELECT
                date_trunc('month', fecha) AS mes,
                departamento,
                depto_codigo,
                grupo,
                alimento,
                SUM(cantidad_kg)            AS cantidad_kg,
                COUNT(*)                    AS n_registros
            FROM "{ABAST_ID}"
            WHERE fecha IS NOT NULL
              AND alimento IS NOT NULL
              AND cantidad_kg IS NOT NULL
              AND cantidad_kg > 0
            GROUP BY 1, 2, 3, 4, 5
        ''',
    ),
]
