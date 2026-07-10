"""FAA Aircraft Registry — one daily ZIP of distinct fixed tables.

https://registry.faa.gov/database/ReleasableAircraft.zip is one daily ZIP whose
member files are distinct fixed tables. We publish MASTER (registration master),
DEREG (deregistration history), ACFTREF (aircraft make/model reference) and
ENGINE (engine reference). Members are BOM-prefixed, comma-delimited,
space-padded text with a trailing comma (an empty final column we drop). Parsed
all-string to preserve leading zeros in codes/N-numbers/zips; the transform SQL
trims and casts.

Both mechanisms are whole-corpus snapshots with no incremental filter, so the
fetch shape is stateless full re-pull + overwrite.
"""

import io
import zipfile
from collections import Counter

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet
from utils import faa_get

_REGISTRY_URL = "https://registry.faa.gov/database/ReleasableAircraft.zip"

# download spec id -> member file inside ReleasableAircraft.zip
_REGISTRY_MEMBERS = {
    "faa-master": "MASTER.txt",
    "faa-dereg": "DEREG.txt",
    "faa-acftref": "ACFTREF.txt",
    "faa-engine": "ENGINE.txt",
    "faa-dealer": "DEALER.txt",
    "faa-docindex": "DOCINDEX.txt",
    "faa-reserved": "RESERVED.txt",
}


def _read_registry_member(zf: zipfile.ZipFile, member: str) -> pa.Table:
    """Parse one registry member by FIXED byte position, not naive comma split.

    The files look CSV-ish but are really fixed-width records joined by commas
    at fixed gap positions; text fields (company names, addresses) contain
    unquoted embedded commas, so a delimiter split miscounts columns. We locate
    the *structural* comma positions (a comma present at the same byte offset in
    ~every row) and slice fields between them — embedded commas then stay inside
    their field. Everything is kept as string to preserve leading zeros in
    codes / N-numbers / zip codes; the transform SQL trims and casts.
    """
    data = zf.read(member)
    if data[:3] == b"\xef\xbb\xbf":  # strip UTF-8 BOM
        data = data[3:]
    lines = data.decode("latin-1").split("\n")
    names = [n.strip() for n in lines[0].rstrip("\r").split(",")]
    while names and names[-1] == "":  # drop trailing empty header from trailing comma
        names.pop()
    ncols = len(names)
    rows = [ln.rstrip("\r") for ln in lines[1:] if ln.strip() != ""]
    if not rows:
        return pa.table([pa.array([], type=pa.string()) for _ in names], names=names)

    # Structural comma offsets: present in (nearly) every sampled row.
    sample = rows[: min(5000, len(rows))]
    counts: Counter = Counter()
    for ln in sample:
        i = ln.find(",")
        while i != -1:
            counts[i] += 1
            i = ln.find(",", i + 1)
    threshold = 0.98 * len(sample)
    positions = sorted(p for p, c in counts.items() if c >= threshold)
    if len(positions) < ncols - 1:
        raise AssertionError(
            f"{member}: found {len(positions)} structural commas for {ncols} columns "
            f"— registry record layout may have changed"
        )

    cols: list[list[str]] = [[] for _ in range(ncols)]
    for ln in rows:
        prev = 0
        for i in range(ncols):
            if i < len(positions):
                end = positions[i]
                cols[i].append(ln[prev:end].strip())
                prev = end + 1
            else:
                cols[i].append(ln[prev:].strip())
    return pa.table([pa.array(c, type=pa.string()) for c in cols], names=names)


def fetch_registry(node_id: str) -> None:
    asset = node_id
    member = _REGISTRY_MEMBERS[node_id]
    resp = faa_get(_REGISTRY_URL)
    with zipfile.ZipFile(io.BytesIO(resp.content)) as zf:
        table = _read_registry_member(zf, member)
    if table.num_rows == 0:
        raise AssertionError(f"{asset}: registry member {member} parsed to 0 rows")
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id=sid, fn=fetch_registry, kind="download") for sid in _REGISTRY_MEMBERS
]


# --- TRANSFORM_SPECS ---------------------------------------------------------
# Each publishes one Delta table. Registry transforms trim the space-padded
# all-string columns and cast dates (YYYYMMDD) / years.

_SQL_MASTER = '''
    SELECT
        TRIM("N-NUMBER")                                      AS n_number,
        TRIM("SERIAL NUMBER")                                 AS serial_number,
        TRIM("MFR MDL CODE")                                  AS mfr_mdl_code,
        TRIM("ENG MFR MDL")                                   AS eng_mfr_mdl_code,
        TRY_CAST(NULLIF(TRIM("YEAR MFR"), '') AS INTEGER)     AS year_mfr,
        TRIM("TYPE REGISTRANT")                               AS type_registrant,
        TRIM("NAME")                                          AS registrant_name,
        TRIM("CITY")                                          AS city,
        TRIM("STATE")                                         AS state,
        TRIM("ZIP CODE")                                      AS zip_code,
        TRIM("COUNTY")                                        AS county,
        TRIM("COUNTRY")                                       AS country,
        TRY_STRPTIME(NULLIF(TRIM("LAST ACTION DATE"), ''), '%Y%m%d')::DATE AS last_action_date,
        TRY_STRPTIME(NULLIF(TRIM("CERT ISSUE DATE"), ''), '%Y%m%d')::DATE  AS cert_issue_date,
        TRIM("CERTIFICATION")                                 AS certification,
        TRIM("TYPE AIRCRAFT")                                 AS type_aircraft,
        TRIM("TYPE ENGINE")                                   AS type_engine,
        TRIM("STATUS CODE")                                   AS status_code,
        TRIM("MODE S CODE")                                   AS mode_s_code,
        TRY_STRPTIME(NULLIF(TRIM("AIR WORTH DATE"), ''), '%Y%m%d')::DATE   AS air_worthiness_date,
        TRY_STRPTIME(NULLIF(TRIM("EXPIRATION DATE"), ''), '%Y%m%d')::DATE  AS expiration_date,
        TRIM("UNIQUE ID")                                     AS unique_id,
        TRIM("KIT MFR")                                       AS kit_mfr,
        TRIM("KIT MODEL")                                     AS kit_model,
        TRIM("MODE S CODE HEX")                               AS mode_s_code_hex
    FROM "faa-master"
    WHERE TRIM("N-NUMBER") <> ''
'''

_SQL_DEREG = '''
    SELECT
        TRIM("N-NUMBER")                                      AS n_number,
        TRIM("SERIAL-NUMBER")                                 AS serial_number,
        TRIM("MFR-MDL-CODE")                                  AS mfr_mdl_code,
        TRIM("STATUS-CODE")                                   AS status_code,
        TRIM("NAME")                                          AS registrant_name,
        TRIM("CITY-MAIL")                                     AS city,
        TRIM("STATE-ABBREV-MAIL")                             AS state,
        TRIM("ZIP-CODE-MAIL")                                 AS zip_code,
        TRIM("COUNTRY-MAIL")                                  AS country,
        TRIM("ENG-MFR-MDL")                                   AS eng_mfr_mdl_code,
        TRY_CAST(NULLIF(TRIM("YEAR-MFR"), '') AS INTEGER)     AS year_mfr,
        TRIM("CERTIFICATION")                                 AS certification,
        TRY_STRPTIME(NULLIF(TRIM("AIR-WORTH-DATE"), ''), '%Y%m%d')::DATE AS air_worthiness_date,
        TRY_STRPTIME(NULLIF(TRIM("CANCEL-DATE"), ''), '%Y%m%d')::DATE    AS cancel_date,
        TRY_STRPTIME(NULLIF(TRIM("LAST-ACT-DATE"), ''), '%Y%m%d')::DATE  AS last_action_date,
        TRY_STRPTIME(NULLIF(TRIM("CERT-ISSUE-DATE"), ''), '%Y%m%d')::DATE AS cert_issue_date,
        TRIM("MODE-S-CODE")                                   AS mode_s_code,
        TRIM("MODE S CODE HEX")                               AS mode_s_code_hex
    FROM "faa-dereg"
    WHERE TRIM("N-NUMBER") <> ''
'''

_SQL_ACFTREF = '''
    SELECT
        TRIM("CODE")                                          AS code,
        TRIM("MFR")                                           AS mfr,
        TRIM("MODEL")                                         AS model,
        TRIM("TYPE-ACFT")                                     AS type_aircraft,
        TRIM("TYPE-ENG")                                      AS type_engine,
        TRIM("AC-CAT")                                        AS aircraft_category,
        TRIM("BUILD-CERT-IND")                                AS build_cert_ind,
        TRY_CAST(NULLIF(TRIM("NO-ENG"), '') AS INTEGER)       AS num_engines,
        TRY_CAST(NULLIF(TRIM("NO-SEATS"), '') AS INTEGER)     AS num_seats,
        TRIM("AC-WEIGHT")                                     AS weight_class,
        TRY_CAST(NULLIF(TRIM("SPEED"), '') AS INTEGER)        AS cruising_speed,
        TRIM("TC-DATA-SHEET")                                 AS tc_data_sheet,
        TRIM("TC-DATA-HOLDER")                                AS tc_data_holder
    FROM "faa-acftref"
    WHERE TRIM("CODE") <> ''
'''

_SQL_ENGINE = '''
    SELECT
        TRIM("CODE")                                          AS code,
        TRIM("MFR")                                           AS mfr,
        TRIM("MODEL")                                         AS model,
        TRIM("TYPE")                                          AS type,
        TRY_CAST(NULLIF(TRIM("HORSEPOWER"), '') AS INTEGER)   AS horsepower,
        TRY_CAST(NULLIF(TRIM("THRUST"), '') AS INTEGER)       AS thrust_lbs
    FROM "faa-engine"
    WHERE TRIM("CODE") <> ''
'''

_REGISTRY_SQL = {
    "faa-master": _SQL_MASTER,
    "faa-dereg": _SQL_DEREG,
    "faa-acftref": _SQL_ACFTREF,
    "faa-engine": _SQL_ENGINE,
}

TRANSFORM_SPECS = [
    SqlNodeSpec(id=f"{sid}-transform", deps=[sid], sql=sql)
    for sid, sql in _REGISTRY_SQL.items()
]
