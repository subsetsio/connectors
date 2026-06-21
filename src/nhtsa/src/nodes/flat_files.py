"""NHTSA ODI flat-file subsets: recalls / complaints / investigations.

These come from the NHTSA Office of Defects Investigation (ODI) flat files:
tab-delimited text, NO header row, columns positional per the published field
dictionaries. They are full-corpus snapshots republished daily, so each fetch
is a stateless full re-pull (overwrite); there is no incremental filter.
Recalls is split into two era zips (PRE_2010 + POST_2010) streamed into one raw
asset. The raw is written as all-string parquet (the flat files are untyped
text); the SQL transform does the typing.

This is one parametric family: a single ``fetch_flat_file(node_id)`` drives all
three subsets from the ``FLAT_SOURCES`` config.
"""

import io
import zipfile

import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    transient_retry,
    raw_parquet_writer,
)


# --------------------------------------------------------------------------- #
# HTTP retry/transport
# --------------------------------------------------------------------------- #
@transient_retry()
def _get_bytes(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp.content


@transient_retry(min_wait=2, max_wait=60)
def _get_json(url: str):
    resp = get(url, timeout=(10.0, 90.0))
    resp.raise_for_status()
    return resp.json()


# --------------------------------------------------------------------------- #
# ODI flat files (recalls / complaints / investigations)
# --------------------------------------------------------------------------- #
RECALLS_COLS = [
    "RECORD_ID", "CAMPNO", "MAKETXT", "MODELTXT", "YEARTXT", "MFGCAMPNO",
    "COMPNAME", "MFGNAME", "BGMAN", "ENDMAN", "RCLTYPECD", "POTAFF", "ODATE",
    "INFLUENCED_BY", "MFGTXT", "RCDATE", "DATEA", "RPNO", "FMVSS",
    "DESC_DEFECT", "CONEQUENCE_DEFECT", "CORRECTIVE_ACTION", "NOTES",
    "RCL_CMPT_ID", "MFR_COMP_NAME", "MFR_COMP_DESC", "MFR_COMP_PTNO",
    "DO_NOT_DRIVE", "PARK_OUTSIDE",
]

COMPLAINTS_COLS = [
    "CMPLID", "ODINO", "MFR_NAME", "MAKETXT", "MODELTXT", "YEARTXT", "CRASH",
    "FAILDATE", "FIRE", "INJURED", "DEATHS", "COMPDESC", "CITY", "STATE",
    "VIN", "DATEA", "LDATE", "MILES", "OCCURENCES", "CDESCR", "CMPL_TYPE",
    "POLICE_RPT_YN", "PURCH_DT", "ORIG_OWNER_YN", "ANTI_BRAKES_YN",
    "CRUISE_CONT_YN", "NUM_CYLS", "DRIVE_TRAIN", "FUEL_SYS", "FUEL_TYPE",
    "TRANS_TYPE", "VEH_SPEED", "DOT", "TIRE_SIZE", "LOC_OF_TIRE",
    "TIRE_FAIL_TYPE", "ORIG_EQUIP_YN", "MANUF_DT", "SEAT_TYPE",
    "RESTRAINT_TYPE", "DEALER_NAME", "DEALER_TEL", "DEALER_CITY",
    "DEALER_STATE", "DEALER_ZIP", "PROD_TYPE", "REPAIRED_YN", "MEDICAL_ATTN",
    "VEHICLES_TOWED_YN", "STATE_OF_INCIDENT", "VEHICLE_OPERATOR",
]

INVESTIGATIONS_COLS = [
    "NHTSA_ACTION_NUMBER", "MAKE", "MODEL", "YEAR", "COMPNAME", "MFR_NAME",
    "ODATE", "CDATE", "CAMPNO", "SUBJECT", "SUMMARY",
]

_FFDD = "https://static.nhtsa.gov/odi/ffdd"
FLAT_SOURCES = {
    "nhtsa-recalls": (
        RECALLS_COLS,
        [f"{_FFDD}/rcl/FLAT_RCL_PRE_2010.zip", f"{_FFDD}/rcl/FLAT_RCL_POST_2010.zip"],
    ),
    "nhtsa-complaints": (
        COMPLAINTS_COLS,
        [f"{_FFDD}/cmpl/FLAT_CMPL.zip"],
    ),
    "nhtsa-investigations": (
        INVESTIGATIONS_COLS,
        [f"{_FFDD}/inv/FLAT_INV.zip"],
    ),
}

_BATCH_ROWS = 25_000


def _iter_lines(zip_bytes: bytes):
    """Yield each record as raw bytes (split strictly on b'\\n').

    The ODI flat files use one physical line per record with no embedded
    newlines (verified by probing: every line splits to the exact field
    count), so splitting only on \\n is correct and keeps memory bounded by
    streaming the single zip member rather than materialising the (up to
    ~1.5GB) decompressed text.
    """
    zf = zipfile.ZipFile(io.BytesIO(zip_bytes))
    name = zf.namelist()[0]
    with zf.open(name) as fh:
        buf = b""
        while True:
            chunk = fh.read(1 << 20)
            if not chunk:
                break
            buf += chunk
            parts = buf.split(b"\n")
            buf = parts.pop()
            for p in parts:
                yield p
        if buf:
            yield buf


def fetch_flat_file(node_id: str) -> None:
    cols, urls = FLAT_SOURCES[node_id]
    n = len(cols)
    schema = pa.schema([(c, pa.string()) for c in cols])

    columns = {c: [] for c in cols}
    size = total = bad = 0

    with raw_parquet_writer(node_id, schema) as writer:
        for url in urls:
            zip_bytes = _get_bytes(url)
            for line in _iter_lines(zip_bytes):
                if line.endswith(b"\r"):
                    line = line[:-1]
                if not line:
                    continue
                cells = line.decode("latin-1").split("\t")
                total += 1
                if len(cells) != n:
                    bad += 1
                for i, c in enumerate(cols):
                    columns[c].append(cells[i] if i < len(cells) else None)
                size += 1
                if size >= _BATCH_ROWS:
                    writer.write_table(pa.table(columns, schema=schema))
                    columns = {c: [] for c in cols}
                    size = 0
        if size:
            writer.write_table(pa.table(columns, schema=schema))

    if total == 0:
        raise RuntimeError(f"{node_id}: parsed 0 records from {urls}")
    if bad / total > 0.05:
        raise RuntimeError(
            f"{node_id}: {bad}/{total} lines had != {n} fields "
            f"(flat-file layout may have changed)"
        )
    print(f"  {node_id}: parsed {total} records ({bad} field-count anomalies)")


# --------------------------------------------------------------------------- #
# Specs
# --------------------------------------------------------------------------- #
DOWNLOAD_SPECS = [
    NodeSpec(id="nhtsa-recalls", fn=fetch_flat_file, kind="download"),
    NodeSpec(id="nhtsa-complaints", fn=fetch_flat_file, kind="download"),
    NodeSpec(id="nhtsa-investigations", fn=fetch_flat_file, kind="download"),
]


_RECALLS_SQL = '''
    SELECT
        TRY_CAST(RECORD_ID AS BIGINT)                              AS record_id,
        NULLIF(TRIM(CAMPNO), '')                                   AS campaign_number,
        NULLIF(TRIM(MAKETXT), '')                                  AS make,
        NULLIF(TRIM(MODELTXT), '')                                 AS model,
        TRY_CAST(NULLIF(YEARTXT, '9999') AS INTEGER)              AS model_year,
        NULLIF(TRIM(COMPNAME), '')                                 AS component,
        NULLIF(TRIM(MFGNAME), '')                                  AS manufacturer,
        TRY_CAST(strptime(NULLIF(RCDATE, ''), '%Y%m%d') AS DATE)  AS recall_date,
        TRY_CAST(strptime(NULLIF(ODATE, ''), '%Y%m%d') AS DATE)   AS owner_notified_date,
        TRY_CAST(POTAFF AS BIGINT)                                 AS potentially_affected,
        NULLIF(TRIM(RCLTYPECD), '')                                AS recall_type,
        NULLIF(TRIM(FMVSS), '')                                    AS fmvss_number,
        NULLIF(DESC_DEFECT, '')                                    AS defect_description,
        NULLIF(CONEQUENCE_DEFECT, '')                              AS defect_consequence,
        NULLIF(CORRECTIVE_ACTION, '')                             AS corrective_action,
        NULLIF(NOTES, '')                                          AS notes,
        DO_NOT_DRIVE                                               AS do_not_drive,
        PARK_OUTSIDE                                               AS park_outside
    FROM "nhtsa-recalls"
    WHERE RECORD_ID IS NOT NULL AND TRIM(RECORD_ID) <> ''
'''

_COMPLAINTS_SQL = '''
    SELECT
        TRY_CAST(CMPLID AS BIGINT)                                 AS complaint_id,
        TRY_CAST(ODINO AS BIGINT)                                  AS odi_number,
        NULLIF(TRIM(MFR_NAME), '')                                 AS manufacturer,
        NULLIF(TRIM(MAKETXT), '')                                  AS make,
        NULLIF(TRIM(MODELTXT), '')                                 AS model,
        TRY_CAST(NULLIF(YEARTXT, '9999') AS INTEGER)             AS model_year,
        NULLIF(TRIM(COMPDESC), '')                                 AS component,
        CRASH                                                      AS crash,
        FIRE                                                       AS fire,
        TRY_CAST(INJURED AS INTEGER)                              AS injured,
        TRY_CAST(DEATHS AS INTEGER)                               AS deaths,
        -- A handful of consumer-entered incident dates are impossible
        -- (e.g. year 2203); an incident cannot post-date "now", so drop those.
        CASE WHEN TRY_CAST(strptime(NULLIF(FAILDATE, ''), '%Y%m%d') AS DATE) <= current_date
             THEN TRY_CAST(strptime(NULLIF(FAILDATE, ''), '%Y%m%d') AS DATE)
        END                                                        AS incident_date,
        TRY_CAST(strptime(NULLIF(DATEA, ''), '%Y%m%d') AS DATE)   AS date_added,
        TRY_CAST(strptime(NULLIF(LDATE, ''), '%Y%m%d') AS DATE)   AS date_filed,
        NULLIF(TRIM(CITY), '')                                     AS city,
        NULLIF(TRIM(STATE), '')                                    AS state,
        TRY_CAST(MILES AS BIGINT)                                  AS miles,
        NULLIF(CDESCR, '')                                         AS description,
        NULLIF(TRIM(CMPL_TYPE), '')                                AS complaint_type,
        NULLIF(TRIM(PROD_TYPE), '')                                AS product_type
    FROM "nhtsa-complaints"
    WHERE CMPLID IS NOT NULL AND TRIM(CMPLID) <> ''
'''

_INVESTIGATIONS_SQL = '''
    SELECT
        NULLIF(TRIM(NHTSA_ACTION_NUMBER), '')                     AS action_number,
        NULLIF(TRIM(MAKE), '')                                    AS make,
        NULLIF(TRIM(MODEL), '')                                   AS model,
        TRY_CAST(NULLIF(YEAR, '9999') AS INTEGER)               AS model_year,
        NULLIF(TRIM(COMPNAME), '')                               AS component,
        NULLIF(TRIM(MFR_NAME), '')                               AS manufacturer,
        TRY_CAST(strptime(NULLIF(ODATE, ''), '%Y%m%d') AS DATE) AS open_date,
        TRY_CAST(strptime(NULLIF(CDATE, ''), '%Y%m%d') AS DATE) AS close_date,
        NULLIF(TRIM(CAMPNO), '')                                 AS related_campaign,
        NULLIF(SUBJECT, '')                                      AS subject,
        NULLIF(SUMMARY, '')                                      AS summary
    FROM "nhtsa-investigations"
    WHERE NHTSA_ACTION_NUMBER IS NOT NULL AND TRIM(NHTSA_ACTION_NUMBER) <> ''
'''

TRANSFORM_SPECS = [
    SqlNodeSpec(id="nhtsa-recalls-transform", deps=["nhtsa-recalls"], sql=_RECALLS_SQL),
    SqlNodeSpec(id="nhtsa-complaints-transform", deps=["nhtsa-complaints"], sql=_COMPLAINTS_SQL),
    SqlNodeSpec(id="nhtsa-investigations-transform", deps=["nhtsa-investigations"], sql=_INVESTIGATIONS_SQL),
]
