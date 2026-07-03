"""INPE Programa Queimadas — active-fire-detection (focos) statistics.

Source: INPE's "dados abertos" Apache autoindex tree on dataserver-coids.inpe.br.
One row per detected fire pixel. There is no upstream catalog API and no
pre-aggregated statistics file, so each published subset is a statistical
fire-activity time series aggregated here from the annual focos CSVs.

Mechanism: per-year bulk download of zipped CSVs, discovered by listing the
Apache directory index (no hardcoded year range — the available years are read
from the listing each run). Fetch shape is **stateless full re-pull** (shape 1):
the whole multi-decade history is a few hundred MB of zips and re-aggregates in
minutes, and the current-year file is rewritten as detections accrue, so trusting
no stored watermark picks up revisions for free.

Two source schemas are used:
  * Reference-satellite annual files (Brasil_sat_ref / AMS_sat_ref): the
    methodologically-consistent single-sensor (AQUA_M-T) comparison series. Columns:
    id_bdq, foco_id, lat, lon, data_pas, pais, estado, municipio, bioma.
    Used for the count tables (state / biome / municipality / country).
  * All-satellite annual files (Brasil_todos_sats): richer schema carrying
    satelite + meteorology/FRP. Filtered to the reference satellite (AQUA_M-T)
    so the national series' fire-radiative-power and fire-risk means are
    available while its counts stay consistent with the reference series
    (verified: AQUA_M-T count == reference-file count).
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
    SqlNodeSpec,
    get,
    save_raw_parquet,
    transient_retry,
)
from constants import (
    AMS_REF_DIR,
    BRASIL_ALLSAT_DIR,
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


def _list_zip_urls(dir_url: str) -> list[str]:
    """Discover the annual zip files in an Apache autoindex directory."""
    index = _download(dir_url if dir_url.endswith("/") else dir_url + "/").decode(
        "utf-8", "replace"
    )
    hrefs = re.findall(r'href="([^"?][^"]*\.zip)"', index)
    urls = sorted(
        {urljoin(dir_url + "/", h) for h in hrefs}
    )
    if not urls:
        raise RuntimeError(f"no .zip files found in directory index: {dir_url}")
    return urls


def _iter_rows(zip_url: str):
    """Yield CSV rows (as dicts) from a single zipped focos file."""
    content = _download(zip_url)
    zf = zipfile.ZipFile(io.BytesIO(content))
    member = zf.namelist()[0]
    with zf.open(member) as fh:
        text = io.TextIOWrapper(fh, encoding="utf-8", newline="")
        yield from csv.DictReader(text)


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
    for url in _list_zip_urls(BRASIL_REF_DIR):
        for row in _iter_rows(url):
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
    for url in _list_zip_urls(BRASIL_REF_DIR):
        for row in _iter_rows(url):
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
    """Annual fire-detection counts per Brazilian municipality (reference series)."""
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
    for url in _list_zip_urls(BRASIL_ALLSAT_DIR):
        for row in _iter_rows(url):
            if row.get("satelite") != REFERENCE_SATELLITE:
                continue
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
    for url in _list_zip_urls(AMS_REF_DIR):
        for row in _iter_rows(url):
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


# ----------------------------------------------------------------------------
# transforms — one published Delta table per subset (thin parse-and-type gate)
# ----------------------------------------------------------------------------
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="inpe-focos-brasil-estado-mensal-transform",
        deps=["inpe-focos-brasil-estado-mensal"],
        sql='''
            SELECT
                CAST(ano AS INTEGER) AS ano,
                CAST(mes AS INTEGER) AS mes,
                estado,
                CAST(n_focos AS BIGINT) AS n_focos
            FROM "inpe-focos-brasil-estado-mensal"
            WHERE estado IS NOT NULL AND n_focos > 0
            ORDER BY ano, mes, estado
        ''',
        key=("ano", "mes", "estado"),
        temporal="ano",
    ),
    SqlNodeSpec(
        id="inpe-focos-brasil-bioma-mensal-transform",
        deps=["inpe-focos-brasil-bioma-mensal"],
        sql='''
            SELECT
                CAST(ano AS INTEGER) AS ano,
                CAST(mes AS INTEGER) AS mes,
                bioma,
                CAST(n_focos AS BIGINT) AS n_focos
            FROM "inpe-focos-brasil-bioma-mensal"
            WHERE bioma IS NOT NULL AND n_focos > 0
            ORDER BY ano, mes, bioma
        ''',
        key=("ano", "mes", "bioma"),
        temporal="ano",
    ),
    SqlNodeSpec(
        id="inpe-focos-brasil-municipio-anual-transform",
        deps=["inpe-focos-brasil-municipio-anual"],
        sql='''
            SELECT
                CAST(ano AS INTEGER) AS ano,
                estado,
                municipio,
                CAST(n_focos AS BIGINT) AS n_focos
            FROM "inpe-focos-brasil-municipio-anual"
            WHERE estado IS NOT NULL AND municipio IS NOT NULL AND n_focos > 0
            ORDER BY ano, estado, municipio
        ''',
        key=("ano", "estado", "municipio"),
        temporal="ano",
    ),
    SqlNodeSpec(
        id="inpe-focos-brasil-mensal-transform",
        deps=["inpe-focos-brasil-mensal"],
        sql='''
            SELECT
                CAST(ano AS INTEGER) AS ano,
                CAST(mes AS INTEGER) AS mes,
                CAST(n_focos AS BIGINT) AS n_focos,
                CAST(frp_medio AS DOUBLE) AS frp_medio,
                CAST(risco_fogo_medio AS DOUBLE) AS risco_fogo_medio,
                CAST(precipitacao_media AS DOUBLE) AS precipitacao_media,
                CAST(dias_sem_chuva_medio AS DOUBLE) AS dias_sem_chuva_medio
            FROM "inpe-focos-brasil-mensal"
            WHERE n_focos > 0
            ORDER BY ano, mes
        ''',
        key=("ano", "mes"),
        temporal="ano",
    ),
    SqlNodeSpec(
        id="inpe-focos-america-sul-pais-mensal-transform",
        deps=["inpe-focos-america-sul-pais-mensal"],
        sql='''
            SELECT
                CAST(ano AS INTEGER) AS ano,
                CAST(mes AS INTEGER) AS mes,
                pais,
                CAST(n_focos AS BIGINT) AS n_focos
            FROM "inpe-focos-america-sul-pais-mensal"
            WHERE pais IS NOT NULL AND n_focos > 0
            ORDER BY ano, mes, pais
        ''',
        key=("ano", "mes", "pais"),
        temporal="ano",
    ),
]
