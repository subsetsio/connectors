"""INPE Programa Queimadas — active-fire-detection (focos) statistics.

Source: INPE's "dados abertos" Apache autoindex tree on dataserver-coids.inpe.br.
One row per detected fire pixel. There is no upstream catalog API and no
pre-aggregated statistics file, so each published subset is a statistical
fire-activity time series aggregated here from the focos CSVs.

Mechanism: bulk download discovered by listing the Apache directory indexes
(no hardcoded year range). Two source layers are combined:

  * Annual archives (csv/anual/...): one zip per CLOSED year. INPE creates a
    year's zip only months after year-end (2025's appeared Feb-2026), so the
    annual layer is authoritative for closed years and never covers the
    current year.
  * Monthly files (csv/mensal/Brasil, csv/mensal/America_Sul): one plain CSV
    per month, published within the month itself. Each series reads the
    monthly files ONLY for years newer than its newest annual zip, so once a
    year's annual archive appears it supersedes the monthly files for that
    year.

Fetch shape is **stateless full re-pull** (shape 1): the whole multi-decade
history is a few hundred MB and re-aggregates in minutes; trusting no stored
watermark picks up upstream revisions (and the annual consolidation of the
monthly layer) for free.

Reference satellite: INPE's cross-year comparison series ("satélite de
referência") is the single sensor AQUA_M-T (AQUA afternoon overpass, since
2002-07-03). Decision 2026-07: AQUA_M-T REMAINS the reference — INPE's
"situação atual" page still labels the official series "Apenas Satélite de
Referência - AQUA Tarde", and the monthly files carry AQUA_M-T detections
through 2026-07 at counts consistent with prior years (e.g. Jun-2026 5,209 vs
Jun-2025 6,060), despite earlier decommissioning announcements. When INPE
does retire AQUA the FAQ designates NPP-SUOMI (VIIRS) as successor with an
explicit series-compatibility adjustment (~10x more detections); the monthly
readers raise if a monthly file contains zero reference-satellite rows, so
that switchover surfaces as a loud failure instead of a silent series break.

Source schemas:
  * Annual reference-satellite files (Brasil_sat_ref / AMS_sat_ref):
    reference-satellite rows only, reduced schema: id_bdq, foco_id, lat, lon,
    data_pas, pais, estado, municipio, bioma. Used for the count tables
    (state / biome / municipality / country).
  * Annual all-satellite files (Brasil_todos_sats): richer schema carrying
    satelite + meteorology/FRP. Filtered to the reference satellite so the
    national series' fire-radiative-power and fire-risk means are available
    while its counts stay consistent with the reference series (verified:
    AQUA_M-T count == reference-file count, incl. all 12 months of 2025).
  * Monthly files (both dirs): all-satellite schema with data_hora_gmt as the
    detection timestamp (id, lat, lon, data_hora_gmt, satelite, municipio,
    estado, pais, ..., numero_dias_sem_chuva, precipitacao, risco_fogo,
    bioma, frp). Filtered to the reference satellite; data_hora_gmt is
    normalized to data_pas so downstream aggregation is layer-agnostic.
"""
import csv
import io
import re
import zipfile
from collections import defaultdict
from urllib.parse import urljoin

import pyarrow as pa
from subsets_utils import (
    NodeSpec,
    get,
    save_raw_parquet,
    transient_retry,
)
from constants import (
    AMS_MENSAL_DIR,
    AMS_REF_DIR,
    BRASIL_ALLSAT_DIR,
    BRASIL_MENSAL_DIR,
    BRASIL_REF_DIR,
    REFERENCE_SATELLITE,
)


# ----------------------------------------------------------------------------
# source access helpers
# ----------------------------------------------------------------------------
@transient_retry()  # 6 attempts, exponential backoff, reraises on exhaustion
def _download(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp.content


def _list_index(dir_url: str, pattern: str) -> list[str]:
    """List hrefs matching `pattern` in an Apache autoindex directory."""
    index = _download(dir_url if dir_url.endswith("/") else dir_url + "/").decode(
        "utf-8", "replace"
    )
    hrefs = re.findall(pattern, index)
    return sorted({urljoin(dir_url + "/", h) for h in hrefs})


def _list_zip_urls(dir_url: str) -> list[str]:
    """Discover the annual zip files in an Apache autoindex directory."""
    urls = _list_index(dir_url, r'href="([^"?][^"]*\.zip)"')
    if not urls:
        raise RuntimeError(f"no .zip files found in directory index: {dir_url}")
    return urls


def _last_annual_year(zip_urls: list[str]) -> int:
    """The newest year covered by the annual archive (from the filenames)."""
    years = []
    for u in zip_urls:
        m = re.search(r"_(\d{4})\.zip$", u)
        if m:
            years.append(int(m.group(1)))
    if not years:
        raise RuntimeError(f"no year-stamped annual zips among: {zip_urls[:3]}")
    return max(years)


def _list_monthly_csv_urls(dir_url: str, after_year: int) -> list[str]:
    """Monthly CSVs (focos_mensal[_br]_YYYYMM.csv) for years > after_year.

    The monthly directories also hold months already consolidated into an
    annual archive; those are skipped so the annual layer stays authoritative
    for closed years.
    """
    urls = []
    for u in _list_index(dir_url, r'href="([^"?][^"]*\.csv)"'):
        m = re.search(r"_(\d{4})(\d{2})\.csv$", u)
        if m and int(m.group(1)) > after_year:
            urls.append(u)
    return urls


def _iter_rows(zip_url: str):
    """Yield CSV rows (as dicts) from a single zipped annual focos file."""
    content = _download(zip_url)
    zf = zipfile.ZipFile(io.BytesIO(content))
    member = zf.namelist()[0]
    with zf.open(member) as fh:
        text = io.TextIOWrapper(fh, encoding="utf-8", newline="")
        yield from csv.DictReader(text)


def _iter_monthly_ref_rows(csv_url: str):
    """Yield reference-satellite rows from one monthly CSV, normalized to the
    annual layout (data_hora_gmt -> data_pas).

    Raises if the file has no reference-satellite rows at all: that is the
    signature of INPE retiring the reference sensor (see module docstring),
    which must fail loudly rather than silently truncating the series.
    """
    content = _download(csv_url)
    text = io.TextIOWrapper(io.BytesIO(content), encoding="utf-8", newline="")
    n_ref = 0
    for row in csv.DictReader(text):
        if row.get("satelite") != REFERENCE_SATELLITE:
            continue
        row["data_pas"] = row.get("data_hora_gmt")
        n_ref += 1
        yield row
    if n_ref == 0:
        raise RuntimeError(
            f"no {REFERENCE_SATELLITE} rows in {csv_url} — INPE may have "
            "switched the reference satellite (FAQ designates NPP-SUOMI/VIIRS "
            "as successor); re-verify the series before updating "
            "REFERENCE_SATELLITE"
        )


def _iter_series_rows(annual_dir: str, monthly_dir: str, annual_is_allsat: bool = False):
    """Yield the full reference-satellite series: every annual archive in
    `annual_dir`, then the monthly files in `monthly_dir` for years the
    annual archive does not yet cover (the current year, and the previous
    year until INPE consolidates it months after year-end)."""
    zip_urls = _list_zip_urls(annual_dir)
    for url in zip_urls:
        for row in _iter_rows(url):
            if annual_is_allsat and row.get("satelite") != REFERENCE_SATELLITE:
                continue
            yield row
    for url in _list_monthly_csv_urls(monthly_dir, after_year=_last_annual_year(zip_urls)):
        yield from _iter_monthly_ref_rows(url)


def _year_month(data_pas: str):
    """Parse 'YYYY-MM-DD HH:MM:SS' -> (year, month). Returns None on garbage."""
    s = (data_pas or "").strip()
    if len(s) < 7 or s[4] != "-":
        return None
    try:
        return int(s[0:4]), int(s[5:7])
    except ValueError:
        return None


def _nonneg_float(raw):
    """Parse a numeric cell; treat blanks and negative sentinels as missing."""
    s = (raw or "").strip()
    if not s:
        return None
    try:
        v = float(s)
    except ValueError:
        return None
    return v if v >= 0 else None


# ----------------------------------------------------------------------------
# fetch functions — one per subset, each writes a small pre-aggregated parquet
# ----------------------------------------------------------------------------
def fetch_estado_mensal(node_id: str) -> None:
    """Monthly fire-detection counts per Brazilian state (reference series)."""
    counts: dict = defaultdict(int)
    for row in _iter_series_rows(BRASIL_REF_DIR, BRASIL_MENSAL_DIR):
        ym = _year_month(row.get("data_pas"))
        estado = (row.get("estado") or "").strip()
        if ym is None or not estado:
            continue
        counts[(ym[0], ym[1], estado)] += 1

    keys = sorted(counts)
    table = pa.table(
        {
            "ano": pa.array([k[0] for k in keys], pa.int32()),
            "mes": pa.array([k[1] for k in keys], pa.int32()),
            "estado": pa.array([k[2] for k in keys], pa.string()),
            "n_focos": pa.array([counts[k] for k in keys], pa.int64()),
        }
    )
    save_raw_parquet(table, node_id)


def fetch_bioma_mensal(node_id: str) -> None:
    """Monthly fire-detection counts per Brazilian biome (reference series)."""
    counts: dict = defaultdict(int)
    for row in _iter_series_rows(BRASIL_REF_DIR, BRASIL_MENSAL_DIR):
        ym = _year_month(row.get("data_pas"))
        bioma = (row.get("bioma") or "").strip()
        if ym is None or not bioma:
            continue
        counts[(ym[0], ym[1], bioma)] += 1

    keys = sorted(counts)
    table = pa.table(
        {
            "ano": pa.array([k[0] for k in keys], pa.int32()),
            "mes": pa.array([k[1] for k in keys], pa.int32()),
            "bioma": pa.array([k[2] for k in keys], pa.string()),
            "n_focos": pa.array([counts[k] for k in keys], pa.int64()),
        }
    )
    save_raw_parquet(table, node_id)


def fetch_municipio_anual(node_id: str) -> None:
    """Annual fire-detection counts per Brazilian municipality (reference series).

    Annual archives only, deliberately: a partial current year would read as a
    misleadingly low annual count at this grain, so the table gains a year
    when INPE consolidates it (months after year-end)."""
    counts: dict = defaultdict(int)
    for url in _list_zip_urls(BRASIL_REF_DIR):
        for row in _iter_rows(url):
            ym = _year_month(row.get("data_pas"))
            estado = (row.get("estado") or "").strip()
            municipio = (row.get("municipio") or "").strip()
            if ym is None or not estado or not municipio:
                continue
            counts[(ym[0], estado, municipio)] += 1

    keys = sorted(counts)
    table = pa.table(
        {
            "ano": pa.array([k[0] for k in keys], pa.int32()),
            "estado": pa.array([k[1] for k in keys], pa.string()),
            "municipio": pa.array([k[2] for k in keys], pa.string()),
            "n_focos": pa.array([counts[k] for k in keys], pa.int64()),
        }
    )
    save_raw_parquet(table, node_id)


def fetch_brasil_mensal(node_id: str) -> None:
    """National monthly fire-detection counts plus mean fire-radiative-power and
    fire-risk/meteorology, from the all-satellite files filtered to the reference
    satellite (keeps counts consistent with the reference series)."""
    # (count, frp_sum, frp_n, risco_sum, risco_n, precip_sum, precip_n, dias_sum, dias_n)
    agg: dict = defaultdict(lambda: [0, 0.0, 0, 0.0, 0, 0.0, 0, 0.0, 0])
    for row in _iter_series_rows(
        BRASIL_ALLSAT_DIR, BRASIL_MENSAL_DIR, annual_is_allsat=True
    ):
        ym = _year_month(row.get("data_pas"))
        if ym is None:
            continue
        a = agg[ym]
        a[0] += 1
        frp = _nonneg_float(row.get("frp"))
        if frp is not None:
            a[1] += frp
            a[2] += 1
        risco = _nonneg_float(row.get("risco_fogo"))
        if risco is not None:
            a[3] += risco
            a[4] += 1
        precip = _nonneg_float(row.get("precipitacao"))
        if precip is not None:
            a[5] += precip
            a[6] += 1
        dias = _nonneg_float(row.get("numero_dias_sem_chuva"))
        if dias is not None:
            a[7] += dias
            a[8] += 1

    keys = sorted(agg)

    def mean(s, n):
        return (s / n) if n else None

    table = pa.table(
        {
            "ano": pa.array([k[0] for k in keys], pa.int32()),
            "mes": pa.array([k[1] for k in keys], pa.int32()),
            "n_focos": pa.array([agg[k][0] for k in keys], pa.int64()),
            "frp_medio": pa.array(
                [mean(agg[k][1], agg[k][2]) for k in keys], pa.float64()
            ),
            "risco_fogo_medio": pa.array(
                [mean(agg[k][3], agg[k][4]) for k in keys], pa.float64()
            ),
            "precipitacao_media": pa.array(
                [mean(agg[k][5], agg[k][6]) for k in keys], pa.float64()
            ),
            "dias_sem_chuva_medio": pa.array(
                [mean(agg[k][7], agg[k][8]) for k in keys], pa.float64()
            ),
        }
    )
    save_raw_parquet(table, node_id)


def fetch_america_sul_pais_mensal(node_id: str) -> None:
    """Monthly fire-detection counts per South American country (reference series)."""
    counts: dict = defaultdict(int)
    for row in _iter_series_rows(AMS_REF_DIR, AMS_MENSAL_DIR):
        ym = _year_month(row.get("data_pas"))
        pais = (row.get("pais") or "").strip()
        if ym is None or not pais:
            continue
        counts[(ym[0], ym[1], pais)] += 1

    keys = sorted(counts)
    table = pa.table(
        {
            "ano": pa.array([k[0] for k in keys], pa.int32()),
            "mes": pa.array([k[1] for k in keys], pa.int32()),
            "pais": pa.array([k[2] for k in keys], pa.string()),
            "n_focos": pa.array([counts[k] for k in keys], pa.int64()),
        }
    )
    save_raw_parquet(table, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="inpe-focos-brasil-estado-mensal", fn=fetch_estado_mensal, kind="download"),
    NodeSpec(id="inpe-focos-brasil-bioma-mensal", fn=fetch_bioma_mensal, kind="download"),
    NodeSpec(id="inpe-focos-brasil-municipio-anual", fn=fetch_municipio_anual, kind="download"),
    NodeSpec(id="inpe-focos-brasil-mensal", fn=fetch_brasil_mensal, kind="download"),
    NodeSpec(
        id="inpe-focos-america-sul-pais-mensal",
        fn=fetch_america_sul_pais_mensal,
        kind="download",
    ),
]
