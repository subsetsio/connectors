"""GLODAPv3 raw downloads.

GLODAP is a static, versioned NCEI accession. Each download fetches one CSV
from the v3 accession, normalizes it to typed parquet, and records the source
HTTP signature so later runs can skip unchanged files.
"""

import os
import tempfile

import duckdb

from subsets_utils import (
    MaintainSpec,
    NodeSpec,
    get_client,
    raw_asset_exists,
    raw_parquet_writer,
    record_source_signature,
    source_unchanged,
    transient_retry,
)


_BASE_URL = "https://www.ncei.noaa.gov/data/oceans/ncei/ocads/data/0315582"

_FILES = {
    "glodap-bottle-data": "GLODAPv3_Merged_Master_File.csv",
    "glodap-cruise-metadata": "GLODAPv3_DOIs.csv",
    "glodap-expocodes": "GLODAPv3_EXPOCODES.csv",
    "glodap-cruise-uncertainties": "GLODAPv3_cruise_uncertainties.csv",
    "glodap-cruise-version-map": "v3_cruises.csv",
}

_BOTTLE_COLUMNS = """
expocode cruise v22023_cruise station cast year month day hour minute latitude
longitude bottomdepth maxsampdepth bottle pressure depth temperature temperaturef
temperatureqc theta constemperature salinity salinityf salinityqc abssalinity
sigma0 sigma1 sigma2 sigma3 sigma4 gamma oxygen oxygenf oxygenqc aou aouf
nitrate nitratef nitrateqc nitrite nitritef silicate silicatef silicateqc
phosphate phosphatef phosphateqc tco2 tco2f tco2qc tco2calc talk talkf talkqc
talkcalc phts25p0 phts25p0f phtsinsitutp phtsinsitutpf ph_tmp ph_scale
phts25p0_calc cfc11 pcfc11 cfc11f cfc11qc cfc12 pcfc12 cfc12f cfc12qc cfc113
pcfc113 cfc113f cfc113qc ccl4 pccl4 ccl4f ccl4qc sf6 psf6 sf6f sf6qc c13
c13f c13qc c14 c14f c14err h3 h3f h3err he3 he3f he3err he hef heerr neon
neonf neonerr o18 o18f toc tocf doc docf don donf tdn tdnf chla chlaf fco2
fco2f fco2temp fco2calc doi region
""".split()

_BOTTLE_INT_COLUMNS = {
    "cruise",
    "v22023_cruise",
    "station",
    "cast",
    "year",
    "month",
    "day",
    "hour",
    "minute",
    "bottle",
    "temperaturef",
    "temperatureqc",
    "salinityf",
    "salinityqc",
    "oxygenf",
    "oxygenqc",
    "aouf",
    "nitratef",
    "nitrateqc",
    "nitritef",
    "silicatef",
    "silicateqc",
    "phosphatef",
    "phosphateqc",
    "tco2f",
    "tco2qc",
    "talkf",
    "talkqc",
    "phts25p0f",
    "phtsinsitutpf",
    "cfc11f",
    "cfc11qc",
    "cfc12f",
    "cfc12qc",
    "cfc113f",
    "cfc113qc",
    "ccl4f",
    "ccl4qc",
    "sf6f",
    "sf6qc",
    "c13f",
    "c13qc",
    "c14f",
    "h3f",
    "he3f",
    "hef",
    "neonf",
    "o18f",
    "tocf",
    "docf",
    "donf",
    "tdnf",
    "chlaf",
    "fco2f",
    "region",
}

_BOTTLE_STRING_COLUMNS = {"expocode", "doi", "ph_scale"}


def _url(asset_id: str) -> str:
    return f"{_BASE_URL}/{_FILES[asset_id]}"


def _quote(name: str) -> str:
    return '"' + name.replace('"', '""') + '"'


def _as_string(source: str, target: str) -> str:
    q = _quote(source)
    return f"NULLIF(NULLIF({q}, '-9999'), '') AS {_quote(target)}"


def _as_double(source: str, target: str) -> str:
    q = _quote(source)
    return f"NULLIF(TRY_CAST({q} AS DOUBLE), -9999.0) AS {_quote(target)}"


def _as_int(source: str, target: str) -> str:
    q = _quote(source)
    return (
        f"CAST(NULLIF(TRY_CAST({q} AS DOUBLE), -9999.0) AS BIGINT) "
        f"AS {_quote(target)}"
    )


def _bottle_select() -> str:
    parts = []
    for col in _BOTTLE_COLUMNS:
        if col in _BOTTLE_STRING_COLUMNS:
            parts.append(_as_string(col, col))
        elif col in _BOTTLE_INT_COLUMNS:
            parts.append(_as_int(col, col))
        else:
            parts.append(_as_double(col, col))
    return ",\n    ".join(parts)


_SELECTS = {
    "glodap-bottle-data": _bottle_select(),
    "glodap-cruise-metadata": ",\n    ".join(
        [
            _as_string("EXPOCODE", "expocode"),
            _as_string("DOI", "doi"),
        ]
    ),
    "glodap-expocodes": _as_string("expocode", "expocode"),
    "glodap-cruise-uncertainties": ",\n    ".join(
        [
            _as_string("EXPOCODE", "expocode"),
            _as_double("oxygen(%)", "oxygen_pct"),
            _as_double("nitrate(%)", "nitrate_pct"),
            _as_double("phosphate(%)", "phosphate_pct"),
            _as_double("silicate(%)", "silicate_pct"),
            _as_double("tco2(umol/kg)", "tco2_umol_kg"),
            _as_double("talk(umol/kg)", "talk_umol_kg"),
            _as_double("salinity", "salinity"),
            _as_double("cfc11(%)", "cfc11_pct"),
            _as_double("cfc12(%)", "cfc12_pct"),
            _as_double("cfc113(%)", "cfc113_pct"),
            _as_double("ccl4(%)", "ccl4_pct"),
            _as_double("sf6(%)", "sf6_pct"),
            _as_int("region", "region"),
        ]
    ),
    "glodap-cruise-version-map": ",\n    ".join(
        [
            _as_string("expocode", "expocode"),
            _as_int("cruise", "cruise"),
            _as_int("v2023", "v2023_cruise"),
        ]
    ),
}


@transient_retry()
def _stream_to(path: str, url: str) -> None:
    with get_client().stream("GET", url, timeout=(10.0, 900.0)) as resp:
        resp.raise_for_status()
        with open(path, "wb") as f:
            for chunk in resp.iter_bytes(chunk_size=1 << 20):
                f.write(chunk)


def _fetch_csv(asset_id: str) -> None:
    url = _url(asset_id)
    fd, tmp = tempfile.mkstemp(prefix=f"{asset_id}_", suffix=".csv")
    os.close(fd)
    try:
        _stream_to(tmp, url)
        con = duckdb.connect()
        try:
            query = (
                f"SELECT\n    {_SELECTS[asset_id]}\n"
                "FROM read_csv(?, all_varchar=true, header=true)"
            )
            reader = con.execute(query, [tmp]).fetch_record_batch()
            with raw_parquet_writer(asset_id, reader.schema) as writer:
                for batch in reader:
                    writer.write_batch(batch)
        finally:
            con.close()
        record_source_signature(asset_id, url)
    finally:
        try:
            os.remove(tmp)
        except OSError:
            pass


def fetch_csv(node_id: str) -> None:
    _fetch_csv(node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="glodap-bottle-data", fn=fetch_csv, kind="download"),
    NodeSpec(id="glodap-cruise-metadata", fn=fetch_csv, kind="download"),
    NodeSpec(id="glodap-cruise-uncertainties", fn=fetch_csv, kind="download"),
    NodeSpec(id="glodap-cruise-version-map", fn=fetch_csv, kind="download"),
    NodeSpec(id="glodap-expocodes", fn=fetch_csv, kind="download"),
]


MAINTAIN_SPECS = [
    MaintainSpec(
        asset_id=asset_id,
        description=(
            "GLODAPv3 is a versioned static NCEI accession; use NCEI "
            "ETag/Last-Modified for unchanged-file skips."
        ),
        check=lambda aid: source_unchanged(aid, _url(aid))
        and raw_asset_exists(aid, "parquet"),
    )
    for asset_id in _FILES
]
