"""NCES connector — IPEDS complete data files.

Mechanism: ipeds_bulk (research). Each entity is one IPEDS survey component
(HD, EFFY, EF*A, C*_A, F*_F1A, GR, SFA, ...). For a component we fetch EVERY
available collection year as a direct bulk ZIP from
`https://nces.ed.gov/ipeds/datacenter/data/{TABLE}{YEAR}.zip` (no auth, stable
IIS static server), unzip the single CSV inside, conform each year to the latest
year's column set, and stream the union of all years to ONE NDJSON raw asset per
component (with a `year` column added). The transform types the keys and
publishes one wide Delta table per component.

Why NDJSON + conform-to-latest-schema: IPEDS column sets drift across ~20+ years
(columns added/removed). We pin the schema to the most recent year and emit every
row with the *same* keys (missing -> "") so DuckDB's read_json sees one stable
column set regardless of which rows it samples. Values are kept as strings (IPEDS
mixes counts, dollars, rates, and categorical codes); the transform casts only the
join keys (UNITID, year).

Year discovery is source-driven: we scan candidate years from next-year down to a
floor and keep whichever return HTTP 200 (404s are skipped) — no hardcoded list of
which years exist. REF_YEAR is only the anchor year baked into the catalog's
table-file names, used to template the per-year filename.

Stateless full re-pull every run: these are static annual file releases with no
incremental filter (research: "no incremental — full corpus per refresh"). The
maintain step gates whether a fetch runs; if invoked, we re-fetch in full.
"""

import csv
import io
import json
import zipfile
from datetime import datetime, timezone


from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    raw_writer,
    transient_retry,
)

DATA_BASE = "https://nces.ed.gov/ipeds/datacenter/data"

# Anchor year present in every catalog table-file name below (the collect
# snapshot was taken against the 2024 collection year). Used only to locate the
# year token when templating per-year filenames — NOT a claim about coverage.
REF_YEAR = 2024

# Earliest collection year IPEDS offers (its own Data Center year dropdown floors
# at 1980). A scan bound, not an assumption: existence is confirmed per-year by GET.
FLOOR_YEAR = 1980

# Stop scanning older years once this many consecutive years 404 after we've seen
# at least one hit (tolerates small internal gaps; IPEDS series are ~contiguous).
MAX_CONSECUTIVE_MISSES = 8

# entity id (collect) -> latest (REF_YEAR) table-file name. Inlined from the
# collect catalog; the spec id is f"nces-{entity_id}".
ENTITY_META = {
    "ipeds-adm": "ADM2024",
    "ipeds-al": "AL2024",
    "ipeds-c-a": "C2024_A",
    "ipeds-c-b": "C2024_B",
    "ipeds-c-c": "C2024_C",
    "ipeds-cdep": "C2024DEP",
    # COST1/COST2/DRVCOST are IPEDS Data Center virtual/custom tables: the
    # catalog lists them but no complete-data-file bulk zip is published for
    # any collection year (verified 404 across 2020-2024 while sibling
    # IC_AY/DRVIC/FLAGS return 200). The fetch fn raises (no files found) and
    # these three carry standing waivers (permanently-dead upstream for the
    # ipeds_bulk mechanism); the table-file names below are the catalog's.
    "ipeds-cost1": "COST1_2024",
    "ipeds-cost2": "COST2_2024",
    "ipeds-drvcost": "DRVCOST2024",
    "ipeds-drvadm": "DRVADM2024",
    "ipeds-drval": "DRVAL2024",
    "ipeds-drvc": "DRVC2024",
    "ipeds-drvef": "DRVEF2024",
    "ipeds-drvef12": "DRVEF122024",
    "ipeds-drvf": "DRVF2024",
    "ipeds-drvgr": "DRVGR2024",
    "ipeds-drvhr": "DRVHR2024",
    "ipeds-drvom": "DRVOM2024",
    "ipeds-eap": "EAP2024",
    "ipeds-efa": "EF2024A",
    "ipeds-efa-dist": "EF2024A_DIST",
    "ipeds-efb": "EF2024B",
    "ipeds-efc": "EF2024C",
    "ipeds-efcp": "EF2024CP",
    "ipeds-efd": "EF2024D",
    "ipeds-effy": "EFFY2024",
    "ipeds-effy-dist": "EFFY2024_DIST",
    "ipeds-effy-hs": "EFFY2024_HS",
    "ipeds-efia": "EFIA2024",
    "ipeds-flags": "FLAGS2024",
    "ipeds-f-f1a": "F2324_F1A",
    "ipeds-f-f2": "F2324_F2",
    "ipeds-f-f3": "F2324_F3",
    "ipeds-gr": "GR2024",
    "ipeds-gr-l2": "GR2024_L2",
    "ipeds-gr-pell-ssl": "GR2024_PELL_SSL",
    "ipeds-gr200": "GR200_24",
    "ipeds-hd": "HD2024",
    "ipeds-ic": "IC2024",
    "ipeds-om": "OM2024",
    "ipeds-s-is": "S2024_IS",
    "ipeds-s-nh": "S2024_NH",
    "ipeds-s-oc": "S2024_OC",
    "ipeds-s-sis": "S2024_SIS",
    "ipeds-sal-is": "SAL2024_IS",
    "ipeds-sal-nis": "SAL2024_NIS",
    "ipeds-sfa": "SFA2324",
    "ipeds-sfav": "SFAV2324",
}

ENTITY_IDS = sorted(ENTITY_META)


# --------------------------------------------------------------------------- #
# HTTP
# --------------------------------------------------------------------------- #


@transient_retry()
def _get_zip(url: str) -> bytes | None:
    """GET a bulk ZIP. Returns its bytes, or None when the file does not exist
    (404 — that year simply isn't published for this component). Transient
    failures (429/5xx/timeouts) are retried; other 4xx propagate as bugs."""
    resp = get(url, timeout=(10.0, 300.0))
    if resp.status_code == 404:
        return None
    resp.raise_for_status()
    return resp.content


# --------------------------------------------------------------------------- #
# Filename templating + CSV parsing
# --------------------------------------------------------------------------- #
def _year_tokens(year: int) -> dict[str, str]:
    return {
        "span": f"{(year - 1) % 100:02d}{year % 100:02d}",  # academic span, e.g. 2024 -> "2324"
        "full": str(year),                                   # e.g. "2024"
        "yy": f"{year % 100:02d}",                           # e.g. "24"
    }


def _filename_for_year(table_file: str, year: int) -> str | None:
    """Map the REF_YEAR table-file name to the given collection year by swapping
    the year token. Picks the most specific token form present (academic span >
    full 4-digit > 2-digit) so e.g. 'F2324_F1A' -> 'F0910_F1A', 'HD2024' ->
    'HD2010', 'GR200_24' -> 'GR200_10'."""
    ref = _year_tokens(REF_YEAR)
    for form in ("span", "full", "yy"):
        tok0 = ref[form]
        if tok0 in table_file:
            return table_file.replace(tok0, _year_tokens(year)[form])
    return None


def _primary_csv_name(names: list[str], table_file: str) -> str | None:
    """Pick the released CSV inside the zip — the one named after the file, NOT
    the '_rv' revised-values companion."""
    want = f"{table_file.lower()}.csv"
    csvs = [n for n in names if n.lower().endswith(".csv")]
    for n in csvs:
        if n.lower() == want:
            return n
    non_rv = [n for n in csvs if "_rv" not in n.lower()]
    if non_rv:
        return non_rv[0]
    return csvs[0] if csvs else None


def _norm(name: str) -> str:
    """Canonical column name. IPEDS header case/quoting drifts across years
    (e.g. 2024 'UNITID' vs 2002 '"unitid"'); normalize so a column maps to the
    same key regardless of vintage."""
    return name.strip().strip('"').strip().upper()


def _read_csv(content: bytes, table_file: str):
    """Yield (header, row_iterator) for the primary CSV in a component zip.
    IPEDS CSVs are latin-1 (institution names carry non-UTF8 bytes)."""
    zf = zipfile.ZipFile(io.BytesIO(content))
    name = _primary_csv_name(zf.namelist(), table_file)
    if name is None:
        raise RuntimeError(f"{table_file}: no CSV member in zip ({zf.namelist()})")
    data = zf.read(name)
    # Some IPEDS CSVs (notably recent collection years) ship a UTF-8 BOM. Strip it
    # before the latin-1 decode, otherwise it corrupts the first header ("UNITID"
    # -> "ï»¿UNITID") and breaks downstream joins / the transform's EXCLUDE.
    if data[:3] == b"\xef\xbb\xbf":
        data = data[3:]
    text = data.decode("latin-1")
    reader = csv.reader(io.StringIO(text))
    header = next(reader)
    return header, reader


def _write_year(f, content: bytes, table_file: str, year: int, columns: list[str]) -> int:
    """Stream one year's rows to the open NDJSON handle, conformed to `columns`
    (the latest year's header). Returns the row count written."""
    header, reader = _read_csv(content, table_file)
    index = {_norm(name): i for i, name in enumerate(header)}
    written = 0
    for row in reader:
        if not row:
            continue
        rec = {}
        for col in columns:
            i = index.get(col)
            rec[col] = (row[i].strip() if i is not None and i < len(row) else "")
        rec["year"] = year
        f.write(json.dumps(rec) + "\n")
        written += 1
    return written


# --------------------------------------------------------------------------- #
# Download
# --------------------------------------------------------------------------- #
def fetch_one(node_id: str) -> None:
    asset = node_id  # the spec id IS the asset name
    entity_id = node_id[len("nces-"):]          # "nces-ipeds-hd" -> "ipeds-hd"
    table_file = ENTITY_META[entity_id]

    ceiling = datetime.now(tz=timezone.utc).year + 1  # catch a just-released next year
    columns: list[str] | None = None
    total_rows = 0
    years_written: list[int] = []
    misses = 0

    with raw_writer(asset, "ndjson.gz", mode="wt", compression="gzip") as f:
        for year in range(ceiling, FLOOR_YEAR - 1, -1):
            fname = _filename_for_year(table_file, year)
            if fname is None:
                raise RuntimeError(f"{asset}: cannot template a filename from {table_file!r}")
            content = _get_zip(f"{DATA_BASE}/{fname}.zip")
            if content is None:
                if years_written:
                    misses += 1
                    if misses >= MAX_CONSECUTIVE_MISSES:
                        break
                continue
            misses = 0
            if columns is None:
                # Latest existing year pins the published column set (normalized so
                # downstream keys are stable across the source's case/quote drift).
                latest_header, _ = _read_csv(content, fname)
                columns = [_norm(h) for h in latest_header]
            n = _write_year(f, content, fname, year, columns)
            total_rows += n
            years_written.append(year)

    if not years_written:
        raise RuntimeError(
            f"{asset}: no IPEDS files found for {table_file!r} "
            f"(scanned {ceiling}..{FLOOR_YEAR})"
        )
    print(
        f"  {asset}: {total_rows} rows across {len(years_written)} years "
        f"({max(years_written)}..{min(years_written)}), {len(columns)} columns"
    )


DOWNLOAD_SPECS = [
    NodeSpec(id=f"nces-{eid}", fn=fetch_one, kind="download")
    for eid in ENTITY_IDS
]


# --------------------------------------------------------------------------- #
# Transform — one wide Delta table per component
# --------------------------------------------------------------------------- #
def _transform_sql(dep_id: str) -> str:
    # Type the join keys; keep every other IPEDS column as published (string).
    return f'''
        SELECT
            TRY_CAST("UNITID" AS BIGINT) AS unitid,
            CAST("year" AS INTEGER)      AS year,
            * EXCLUDE ("UNITID", "year")
        FROM "{dep_id}"
    '''


TRANSFORM_SPECS = [
    SqlNodeSpec(id=f"{s.id}-transform", deps=[s.id], sql=_transform_sql(s.id), temporal="year")
    for s in DOWNLOAD_SPECS
]
