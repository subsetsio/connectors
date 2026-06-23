"""GLODAP connector — GLODAPv2 merged ocean biogeochemical bottle data product.

One subset: `glodap-bottle-data`, the global GLODAPv2.2023 Merged Master File
(one row per discrete water-bottle sample, full ocean depth, 1972-2021).

Strategy: stateless full re-pull. GLODAP is a versioned static release (a new
NCEI accession is minted per version, e.g. 0283442 for v2.2023); there is no
incremental query, so we re-fetch the single ~853MB master CSV each refresh and
overwrite.

The download streams the CSV to a scratch file, then uses DuckDB to read it as
all-VARCHAR (so a column that is mostly the -9999 sentinel can't be mis-sniffed
as an integer and then error on a decimal row), TRY_CASTs every column to its
proper type, maps the -9999 missing-value sentinel to NULL, and streams the
typed result into a raw parquet (bounded memory). The transform is a thin
passthrough that publishes that typed table.
"""
import os
import tempfile

import duckdb

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get_client,
    transient_retry,
    raw_parquet_writer,
)

# GLODAPv2.2023 NCEI accession directory (persistent, no auth).
_MASTER_URL = (
    "https://www.ncei.noaa.gov/data/oceans/ncei/ocads/data/0283442/"
    "GLODAPv2.2023_Merged_Master_File.csv"
)

# Typed projection over the raw G2-prefixed CSV columns: strip the G2 prefix,
# cast to the proper type, and turn the -9999 missing-value sentinel into NULL.
_TYPED_SELECT = '''
                "G2expocode" AS "expocode",
                NULLIF(TRY_CAST("G2cruise" AS BIGINT), -9999) AS "cruise",
                NULLIF(TRY_CAST("G2station" AS BIGINT), -9999) AS "station",
                NULLIF(TRY_CAST("G2region" AS BIGINT), -9999) AS "region",
                NULLIF(TRY_CAST("G2cast" AS BIGINT), -9999) AS "cast",
                NULLIF(TRY_CAST("G2year" AS BIGINT), -9999) AS "year",
                NULLIF(TRY_CAST("G2month" AS BIGINT), -9999) AS "month",
                NULLIF(TRY_CAST("G2day" AS BIGINT), -9999) AS "day",
                NULLIF(TRY_CAST("G2hour" AS BIGINT), -9999) AS "hour",
                NULLIF(TRY_CAST("G2minute" AS BIGINT), -9999) AS "minute",
                NULLIF(TRY_CAST("G2latitude" AS DOUBLE), -9999) AS "latitude",
                NULLIF(TRY_CAST("G2longitude" AS DOUBLE), -9999) AS "longitude",
                NULLIF(TRY_CAST("G2bottomdepth" AS DOUBLE), -9999) AS "bottomdepth",
                NULLIF(TRY_CAST("G2maxsampdepth" AS DOUBLE), -9999) AS "maxsampdepth",
                NULLIF(TRY_CAST("G2bottle" AS BIGINT), -9999) AS "bottle",
                NULLIF(TRY_CAST("G2pressure" AS DOUBLE), -9999) AS "pressure",
                NULLIF(TRY_CAST("G2depth" AS DOUBLE), -9999) AS "depth",
                NULLIF(TRY_CAST("G2temperature" AS DOUBLE), -9999) AS "temperature",
                NULLIF(TRY_CAST("G2theta" AS DOUBLE), -9999) AS "theta",
                NULLIF(TRY_CAST("G2salinity" AS DOUBLE), -9999) AS "salinity",
                NULLIF(TRY_CAST("G2salinityf" AS BIGINT), -9999) AS "salinityf",
                NULLIF(TRY_CAST("G2salinityqc" AS BIGINT), -9999) AS "salinityqc",
                NULLIF(TRY_CAST("G2sigma0" AS DOUBLE), -9999) AS "sigma0",
                NULLIF(TRY_CAST("G2sigma1" AS DOUBLE), -9999) AS "sigma1",
                NULLIF(TRY_CAST("G2sigma2" AS DOUBLE), -9999) AS "sigma2",
                NULLIF(TRY_CAST("G2sigma3" AS DOUBLE), -9999) AS "sigma3",
                NULLIF(TRY_CAST("G2sigma4" AS DOUBLE), -9999) AS "sigma4",
                NULLIF(TRY_CAST("G2gamma" AS DOUBLE), -9999) AS "gamma",
                NULLIF(TRY_CAST("G2oxygen" AS DOUBLE), -9999) AS "oxygen",
                NULLIF(TRY_CAST("G2oxygenf" AS BIGINT), -9999) AS "oxygenf",
                NULLIF(TRY_CAST("G2oxygenqc" AS BIGINT), -9999) AS "oxygenqc",
                NULLIF(TRY_CAST("G2aou" AS DOUBLE), -9999) AS "aou",
                NULLIF(TRY_CAST("G2aouf" AS BIGINT), -9999) AS "aouf",
                NULLIF(TRY_CAST("G2nitrate" AS DOUBLE), -9999) AS "nitrate",
                NULLIF(TRY_CAST("G2nitratef" AS BIGINT), -9999) AS "nitratef",
                NULLIF(TRY_CAST("G2nitrateqc" AS BIGINT), -9999) AS "nitrateqc",
                NULLIF(TRY_CAST("G2nitrite" AS DOUBLE), -9999) AS "nitrite",
                NULLIF(TRY_CAST("G2nitritef" AS BIGINT), -9999) AS "nitritef",
                NULLIF(TRY_CAST("G2silicate" AS DOUBLE), -9999) AS "silicate",
                NULLIF(TRY_CAST("G2silicatef" AS BIGINT), -9999) AS "silicatef",
                NULLIF(TRY_CAST("G2silicateqc" AS BIGINT), -9999) AS "silicateqc",
                NULLIF(TRY_CAST("G2phosphate" AS DOUBLE), -9999) AS "phosphate",
                NULLIF(TRY_CAST("G2phosphatef" AS BIGINT), -9999) AS "phosphatef",
                NULLIF(TRY_CAST("G2phosphateqc" AS BIGINT), -9999) AS "phosphateqc",
                NULLIF(TRY_CAST("G2tco2" AS DOUBLE), -9999) AS "tco2",
                NULLIF(TRY_CAST("G2tco2f" AS BIGINT), -9999) AS "tco2f",
                NULLIF(TRY_CAST("G2tco2qc" AS BIGINT), -9999) AS "tco2qc",
                NULLIF(TRY_CAST("G2talk" AS DOUBLE), -9999) AS "talk",
                NULLIF(TRY_CAST("G2talkf" AS BIGINT), -9999) AS "talkf",
                NULLIF(TRY_CAST("G2talkqc" AS BIGINT), -9999) AS "talkqc",
                NULLIF(TRY_CAST("G2fco2" AS DOUBLE), -9999) AS "fco2",
                NULLIF(TRY_CAST("G2fco2f" AS BIGINT), -9999) AS "fco2f",
                NULLIF(TRY_CAST("G2fco2temp" AS DOUBLE), -9999) AS "fco2temp",
                NULLIF(TRY_CAST("G2phts25p0" AS DOUBLE), -9999) AS "phts25p0",
                NULLIF(TRY_CAST("G2phts25p0f" AS BIGINT), -9999) AS "phts25p0f",
                NULLIF(TRY_CAST("G2phtsinsitutp" AS DOUBLE), -9999) AS "phtsinsitutp",
                NULLIF(TRY_CAST("G2phtsinsitutpf" AS BIGINT), -9999) AS "phtsinsitutpf",
                NULLIF(TRY_CAST("G2phtsqc" AS BIGINT), -9999) AS "phtsqc",
                NULLIF(TRY_CAST("G2cfc11" AS DOUBLE), -9999) AS "cfc11",
                NULLIF(TRY_CAST("G2pcfc11" AS DOUBLE), -9999) AS "pcfc11",
                NULLIF(TRY_CAST("G2cfc11f" AS BIGINT), -9999) AS "cfc11f",
                NULLIF(TRY_CAST("G2cfc11qc" AS BIGINT), -9999) AS "cfc11qc",
                NULLIF(TRY_CAST("G2cfc12" AS DOUBLE), -9999) AS "cfc12",
                NULLIF(TRY_CAST("G2pcfc12" AS DOUBLE), -9999) AS "pcfc12",
                NULLIF(TRY_CAST("G2cfc12f" AS BIGINT), -9999) AS "cfc12f",
                NULLIF(TRY_CAST("G2cfc12qc" AS BIGINT), -9999) AS "cfc12qc",
                NULLIF(TRY_CAST("G2cfc113" AS DOUBLE), -9999) AS "cfc113",
                NULLIF(TRY_CAST("G2pcfc113" AS DOUBLE), -9999) AS "pcfc113",
                NULLIF(TRY_CAST("G2cfc113f" AS BIGINT), -9999) AS "cfc113f",
                NULLIF(TRY_CAST("G2cfc113qc" AS BIGINT), -9999) AS "cfc113qc",
                NULLIF(TRY_CAST("G2ccl4" AS DOUBLE), -9999) AS "ccl4",
                NULLIF(TRY_CAST("G2pccl4" AS DOUBLE), -9999) AS "pccl4",
                NULLIF(TRY_CAST("G2ccl4f" AS BIGINT), -9999) AS "ccl4f",
                NULLIF(TRY_CAST("G2ccl4qc" AS BIGINT), -9999) AS "ccl4qc",
                NULLIF(TRY_CAST("G2sf6" AS DOUBLE), -9999) AS "sf6",
                NULLIF(TRY_CAST("G2psf6" AS DOUBLE), -9999) AS "psf6",
                NULLIF(TRY_CAST("G2sf6f" AS BIGINT), -9999) AS "sf6f",
                NULLIF(TRY_CAST("G2sf6qc" AS BIGINT), -9999) AS "sf6qc",
                NULLIF(TRY_CAST("G2c13" AS DOUBLE), -9999) AS "c13",
                NULLIF(TRY_CAST("G2c13f" AS BIGINT), -9999) AS "c13f",
                NULLIF(TRY_CAST("G2c13qc" AS BIGINT), -9999) AS "c13qc",
                NULLIF(TRY_CAST("G2c14" AS DOUBLE), -9999) AS "c14",
                NULLIF(TRY_CAST("G2c14f" AS BIGINT), -9999) AS "c14f",
                NULLIF(TRY_CAST("G2c14err" AS DOUBLE), -9999) AS "c14err",
                NULLIF(TRY_CAST("G2h3" AS DOUBLE), -9999) AS "h3",
                NULLIF(TRY_CAST("G2h3f" AS BIGINT), -9999) AS "h3f",
                NULLIF(TRY_CAST("G2h3err" AS DOUBLE), -9999) AS "h3err",
                NULLIF(TRY_CAST("G2he3" AS DOUBLE), -9999) AS "he3",
                NULLIF(TRY_CAST("G2he3f" AS BIGINT), -9999) AS "he3f",
                NULLIF(TRY_CAST("G2he3err" AS DOUBLE), -9999) AS "he3err",
                NULLIF(TRY_CAST("G2he" AS DOUBLE), -9999) AS "he",
                NULLIF(TRY_CAST("G2hef" AS BIGINT), -9999) AS "hef",
                NULLIF(TRY_CAST("G2heerr" AS DOUBLE), -9999) AS "heerr",
                NULLIF(TRY_CAST("G2neon" AS DOUBLE), -9999) AS "neon",
                NULLIF(TRY_CAST("G2neonf" AS BIGINT), -9999) AS "neonf",
                NULLIF(TRY_CAST("G2neonerr" AS DOUBLE), -9999) AS "neonerr",
                NULLIF(TRY_CAST("G2o18" AS DOUBLE), -9999) AS "o18",
                NULLIF(TRY_CAST("G2o18f" AS BIGINT), -9999) AS "o18f",
                NULLIF(TRY_CAST("G2toc" AS DOUBLE), -9999) AS "toc",
                NULLIF(TRY_CAST("G2tocf" AS BIGINT), -9999) AS "tocf",
                NULLIF(TRY_CAST("G2doc" AS DOUBLE), -9999) AS "doc",
                NULLIF(TRY_CAST("G2docf" AS BIGINT), -9999) AS "docf",
                NULLIF(TRY_CAST("G2don" AS DOUBLE), -9999) AS "don",
                NULLIF(TRY_CAST("G2donf" AS BIGINT), -9999) AS "donf",
                NULLIF(TRY_CAST("G2tdn" AS DOUBLE), -9999) AS "tdn",
                NULLIF(TRY_CAST("G2tdnf" AS BIGINT), -9999) AS "tdnf",
                NULLIF(TRY_CAST("G2chla" AS DOUBLE), -9999) AS "chla",
                NULLIF(TRY_CAST("G2chlaf" AS BIGINT), -9999) AS "chlaf",
                "G2doi" AS "doi"
'''


@transient_retry()
def _stream_to(path: str, url: str) -> None:
    """Stream a (large) file to a local scratch path. Re-opened fresh each
    retry so a mid-stream failure can't leave a half-written file behind."""
    with get_client().stream("GET", url, timeout=(10.0, 300.0)) as resp:
        resp.raise_for_status()
        with open(path, "wb") as f:
            for chunk in resp.iter_bytes(chunk_size=1 << 20):
                f.write(chunk)


def fetch_bottle_data(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    fd, tmp = tempfile.mkstemp(prefix="glodap_master_", suffix=".csv")
    os.close(fd)
    try:
        _stream_to(tmp, _MASTER_URL)
        con = duckdb.connect()
        try:
            query = (
                "SELECT\n" + _TYPED_SELECT + "\n"
                "FROM read_csv(?, all_varchar=true, header=true)"
            )
            reader = con.execute(query, [tmp]).fetch_record_batch()
            with raw_parquet_writer(asset, reader.schema) as w:
                for batch in reader:
                    w.write_batch(batch)
        finally:
            con.close()
    finally:
        try:
            os.remove(tmp)
        except OSError:
            pass


DOWNLOAD_SPECS = [
    NodeSpec(id="glodap-bottle-data", fn=fetch_bottle_data, kind="download"),
]


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="glodap-bottle-data-transform",
        deps=["glodap-bottle-data"],
        sql='SELECT * FROM "glodap-bottle-data"',
    ),
]
