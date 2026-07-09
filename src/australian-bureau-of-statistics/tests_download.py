"""Health invariants for the ABS SDMX downloads.

Each download writes one dataflow's full SDMX-CSV as parquet. These tests catch
silent degradation that file existence alone misses: empty payloads, a response
that switched away from SDMX-CSV (losing the stable DATAFLOW/TIME_PERIOD/
OBS_VALUE columns), or dimension codes coerced to integers (which would strip
the leading zeros off postal areas and SA2 codes).

Assets are inspected through parquet metadata rather than `load_raw_parquet`:
the largest dataflow is a 2.86 GB CSV, and materializing every asset as an
Arrow table would OOM the runner these tests run on.
"""

import pyarrow as pa
import pyarrow.parquet as pq

from subsets_utils import raw_parquet_localpath

# Columns SDMX-CSV carries regardless of the dataflow's DSD. Everything else —
# including OBS_STATUS and UNIT_MEASURE — is flow-dependent (C21_G01_POA, for
# instance, has neither).
_STABLE_COLS = {"DATAFLOW", "TIME_PERIOD", "OBS_VALUE"}


def _assets(spec_ids):
    """Yield (spec_id, parquet metadata, arrow schema) for every raw asset."""
    for sid in spec_ids:
        with raw_parquet_localpath(sid) as path:
            pf = pq.ParquetFile(path)
            yield sid, pf.metadata, pf.schema_arrow


def test_every_asset_has_rows(spec_ids):
    """An empty asset means the endpoint switched format or the flow was
    silently withdrawn — both look like success to the DAG."""
    for sid, meta, _ in _assets(spec_ids):
        assert meta.num_rows > 0, f"{sid}: raw parquet has 0 rows"


def test_stable_sdmx_columns_present(spec_ids):
    """The stable SDMX-CSV columns must be present on every asset; their
    absence means the response was not the expected flat observation table."""
    for sid, _, schema in _assets(spec_ids):
        missing = _STABLE_COLS - set(schema.names)
        assert not missing, f"{sid}: missing stable SDMX columns {missing}"


def test_dimension_codes_are_strings(spec_ids):
    """Every column except OBS_VALUE must be a string. ABS dimension codes are
    numeric-looking but not numbers: inferring int64 would turn postal area
    '0800' into 800 and silently corrupt every join against a geography."""
    for sid, _, schema in _assets(spec_ids):
        for field in schema:
            if field.name == "OBS_VALUE":
                continue
            assert field.type == pa.string(), (
                f"{sid}: column {field.name} is {field.type}, expected string"
            )
