"""Banco de Espana statistics connector.

Mechanism: bulk_csv_zip (research-chosen, suitability 92). The source publishes
its whole statistics corpus as per-publication ZIPs of wide CSVs plus, per
publication, a series catalogue CSV. Two entities:

- `series` : the series catalogue (one row per series, rich metadata).
- `values` : long-format observations for every series.

The CSVs are Latin-1 encoded and TRANSPOSED (series run across columns; the
first column holds 6 metadata rows -- CODIGO/NUMERO/ALIAS/DESCRIPCION x2/
FRECUENCIA -- then one row per period, then FUENTE/NOTAS footer rows). SQL can
not read that shape, so the download fns unpivot to clean long-format parquet
and the transforms are thin cast/dedup passes.

Strategy: stateless full re-pull. The whole corpus is only low tens of MB
zipped and there is no incremental/since filter on the bulk path, so every run
re-fetches everything and overwrites. We read the 5 PUBLICATION ZIPs (not the
TE_* theme ZIPs, which merely re-bundle the same files) -- these cover the full
catalogue. Cross-publication duplicates (a rate that appears in both `be` and
`ti`) are deduped in the transform SQL for `values` and in-fetch for `series`.
"""

import csv
import io
import re
import zipfile

import pyarrow as pa
from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    transient_retry,
    raw_parquet_writer,
    save_raw_parquet,
)

ZIP_BASE = "https://www.bde.es/webbe/es/estadisticas/compartido/datos/zip"
CSV_BASE = "https://www.bde.es/webbe/es/estadisticas/compartido/datos/csv"

# Publication ids -> human label. These 5 ZIPs / catalogues cover the whole
# Banco de Espana statistics corpus.
PUBLICATIONS = {
    "be": "Boletin Estadistico",
    "si": "Indicadores economicos",
    "ti": "Tipos de interes (daily)",
    "tc": "Tipos de cambio (daily)",
    "pb": "Encuesta sobre prestamos bancarios",
}

# Spanish 3-letter month abbreviations -> month number.
MONTHS = {
    "ENE": 1, "FEB": 2, "MAR": 3, "ABR": 4, "MAY": 5, "JUN": 6,
    "JUL": 7, "AGO": 8, "SEP": 9, "OCT": 10, "NOV": 11, "DIC": 12,
}
# Period label formats: "01 ENE 1999"/"01 ENE1999" (daily), "ENE 1990" /
# "MAR 1995" (monthly & quarterly use end-of-quarter month), "1995" (annual).
RE_DAILY = re.compile(r"^(\d{1,2})\s+([A-Z]{3})\.?\s*(\d{4})$")
RE_MONTH = re.compile(r"^([A-Z]{3})\.?\s*(\d{4})$")
RE_YEAR = re.compile(r"^(\d{4})$")

VALUES_SCHEMA = pa.schema([
    ("series_code", pa.string()),
    ("date", pa.date32()),
    ("value", pa.float64()),
    ("frequency", pa.string()),
    ("period_label", pa.string()),
    ("publication", pa.string()),
])

# Catalogue column order (17 columns, Latin-1) mapped to clean names.
CATALOG_COLUMNS = [
    "series_code", "sequential_number", "alias", "value_file", "description",
    "variable_type", "units_code", "exponent", "decimals", "units_description",
    "frequency", "first_observation", "last_observation", "num_observations",
    "title", "source", "notes",
]
SERIES_SCHEMA = pa.schema([(c, pa.string()) for c in CATALOG_COLUMNS] +
                          [("publication", pa.string())])

import datetime as _dt


def _parse_period(label):
    """Parse a Spanish period label to a datetime.date, or None if not a period
    row (metadata/footer labels like FUENTE/NOTAS return None)."""
    label = label.strip().upper()
    m = RE_DAILY.match(label)
    if m:
        d, mon, y = m.groups()
        if mon in MONTHS:
            try:
                return _dt.date(int(y), MONTHS[mon], int(d))
            except ValueError:
                return None
    m = RE_MONTH.match(label)
    if m:
        mon, y = m.groups()
        if mon in MONTHS:
            return _dt.date(int(y), MONTHS[mon], 1)
    m = RE_YEAR.match(label)
    if m:
        return _dt.date(int(m.group(1)), 1, 1)
    return None


def _parse_value(raw):
    raw = raw.strip()
    if raw in ("", "_"):
        return None
    try:
        return float(raw)
    except ValueError:
        try:
            return float(raw.replace(",", "."))
        except ValueError:
            return None


@transient_retry()
def _fetch_bytes(url):
    resp = get(url, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp.content


def _parse_value_csv(text, publication, alias_to_code, code_to_freq):
    """Unpivot one wide value CSV into long rows.

    Two header layouts exist in the corpus: the common one leads with a CODIGO
    row and carries a FRECUENCIA row; ~96 BE tables instead lead with an
    (unlabelled) ALIAS row and omit both the CODIGO label and the FRECUENCIA
    row. So we treat the FIRST non-empty header row as the identifier row
    regardless of its label, scan the remaining header rows for FRECUENCIA, and
    take data to begin at the first row whose first column parses as a period.
    Identifiers resolve to the canonical catalogue series code (an alias is
    mapped to its code), and missing inline frequency is backfilled from the
    catalogue. This is robust to header-row count and ordering.
    """
    rows = list(csv.reader(io.StringIO(text)))
    if not rows:
        return []
    id_row = freq_row = None
    data_start = None
    for idx, r in enumerate(rows):
        if not r or not any(c.strip() for c in r):
            continue
        if _parse_period(r[0].strip()) is not None:
            data_start = idx
            break
        cells = [c.strip() for c in r[1:]]
        if id_row is None:
            id_row = cells  # first header row holds the per-column identifiers
        elif "FRECUENCIA" in r[0].strip().upper():
            freq_row = cells
    if data_start is None or id_row is None:
        return []

    ids, freqs = [], []
    for i, raw_id in enumerate(id_row):
        # raw_id is a canonical code in standard files, an alias in the ~96
        # alias-led files. Keep it if it's already a known code, else map.
        ident = raw_id if raw_id in code_to_freq else alias_to_code.get(raw_id, raw_id)
        ids.append(ident)
        f = freq_row[i] if freq_row and i < len(freq_row) else ""
        freqs.append(f or code_to_freq.get(ident) or None)

    out = []
    for r in rows[data_start:]:
        if not r:
            continue
        label = r[0].strip()
        date = _parse_period(label)
        if date is None:  # FUENTE / NOTAS footer rows and any stray labels
            continue
        for i, ident in enumerate(ids):
            if not ident:
                continue
            val = _parse_value(r[i + 1]) if i + 1 < len(r) else None
            if val is None:
                continue
            out.append({
                "series_code": ident,
                "date": date,
                "value": val,
                "frequency": freqs[i],
                "period_label": label,
                "publication": publication,
            })
    return out


def _load_catalogue_maps():
    """Build alias->canonical-code and code->frequency maps from the catalogue
    CSVs, so value files that carry only an alias (and no inline frequency) can
    be resolved to the canonical series code and frequency."""
    alias_to_code, code_to_freq = {}, {}
    for pub in PUBLICATIONS:
        text = _fetch_bytes(f"{CSV_BASE}/catalogo_{pub}.csv").decode("latin-1")
        for r in list(csv.reader(io.StringIO(text)))[1:]:
            if not r or not r[0].strip():
                continue
            code = r[0].strip()
            alias = r[2].strip() if len(r) > 2 else ""
            freq = r[10].strip() if len(r) > 10 else ""
            if alias:
                alias_to_code.setdefault(alias, code)
            if freq:
                code_to_freq.setdefault(code, freq)
    return alias_to_code, code_to_freq


def fetch_values(node_id: str) -> None:
    """Download every publication ZIP, unpivot every value CSV to long format,
    stream to one parquet asset (batch per CSV file to bound memory)."""
    asset = node_id
    total = 0
    alias_to_code, code_to_freq = _load_catalogue_maps()
    with raw_parquet_writer(asset, VALUES_SCHEMA) as writer:
        for pub in PUBLICATIONS:
            content = _fetch_bytes(f"{ZIP_BASE}/{pub}.zip")
            zf = zipfile.ZipFile(io.BytesIO(content))
            names = [n for n in zf.namelist()
                     if n.lower().endswith(".csv")
                     and not n.lower().startswith("catalogo")]
            for name in names:
                text = zf.read(name).decode("latin-1")
                rows = _parse_value_csv(text, pub, alias_to_code, code_to_freq)
                if not rows:
                    continue
                table = pa.Table.from_pylist(rows, schema=VALUES_SCHEMA)
                writer.write_table(table)
                total += len(rows)
    if total == 0:
        raise AssertionError(f"{asset}: parsed 0 observations across all ZIPs")
    print(f"  {asset}: wrote {total} observations")


def fetch_series(node_id: str) -> None:
    """Download every publication catalogue CSV, parse to one row per series,
    dedupe by series code across publications, write parquet."""
    asset = node_id
    seen = {}
    for pub in PUBLICATIONS:
        text = _fetch_bytes(f"{CSV_BASE}/catalogo_{pub}.csv").decode("latin-1")
        reader = csv.reader(io.StringIO(text))
        data_rows = list(reader)[1:]  # drop header
        for r in data_rows:
            if not r or not r[0].strip():
                continue
            rec = {CATALOG_COLUMNS[i]: (r[i].strip() if i < len(r) else None)
                   for i in range(len(CATALOG_COLUMNS))}
            rec["publication"] = pub
            code = rec["series_code"]
            if code not in seen:  # first publication wins; dedup across pubs
                seen[code] = rec
    rows = list(seen.values())
    if not rows:
        raise AssertionError(f"{asset}: parsed 0 catalogue rows")
    table = pa.Table.from_pylist(rows, schema=SERIES_SCHEMA)
    save_raw_parquet(table, asset)
    print(f"  {asset}: wrote {len(rows)} series")


DOWNLOAD_SPECS = [
    NodeSpec(id="banco-de-espa-a-series", fn=fetch_series, kind="download"),
    NodeSpec(id="banco-de-espa-a-values", fn=fetch_values, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="banco-de-espa-a-series-transform",
        deps=["banco-de-espa-a-series"],
        sql='''
            SELECT
                series_code,
                alias,
                title,
                description,
                frequency,
                units_description,
                variable_type,
                units_code,
                TRY_CAST(exponent AS INTEGER)         AS exponent,
                TRY_CAST(decimals AS INTEGER)         AS decimals,
                TRY_CAST(num_observations AS INTEGER) AS num_observations,
                first_observation,
                last_observation,
                source,
                notes,
                publication
            FROM "banco-de-espa-a-series"
            WHERE series_code IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="banco-de-espa-a-values-transform",
        deps=["banco-de-espa-a-values"],
        sql='''
            SELECT
                series_code,
                CAST(date AS DATE)   AS date,
                CAST(value AS DOUBLE) AS value,
                frequency,
                publication
            FROM "banco-de-espa-a-values"
            WHERE series_code IS NOT NULL
              AND date IS NOT NULL
              AND value IS NOT NULL
            QUALIFY row_number() OVER (
                PARTITION BY series_code, date ORDER BY value
            ) = 1
        ''',
    ),
]
