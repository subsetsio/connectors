"""Health invariants for the Bundesbank raw assets.

These run post-DAG, in-connector, against the parquet the fetch fns wrote. They
target the silent degradations that file existence alone misses: a dataflow that
parsed to nothing, a header-block change that shifted every column, and above all
a regression in how the two German missing-value sentinels are read.
"""

import pyarrow as pa
import pyarrow.compute as pc
from subsets_utils import load_raw_parquet

EXPECTED_COLUMNS = {
    "dataflow", "file_key", "frequency", "series_key", "label", "time_period",
    "period_start", "value", "flag", "unit", "unit_en", "magnitude", "decimals",
    "category", "last_update", "attributes",
}

# The source's own flag text for "nothing present" (an exact zero) and for the two
# ways a value can be absent. See MISSING_VALUES in the node module.
FLAG_EXACT_ZERO = "Nichts vorhanden"
FLAGS_MEANING_ABSENT = ("Kein Wert vorhanden", "Fehlender Wert (unterdrückt)")


def _strings(table: pa.Table, column: str) -> pa.ChunkedArray:
    """Decode a dictionary-encoded column to plain strings for comparison."""
    return table.column(column).cast(pa.string())


def test_raw_assets_are_wellformed(spec_ids):
    """Each dataflow parsed to a non-empty table with the declared columns, and
    every row carries the identity a transform keys off."""
    for spec_id in spec_ids:
        table = load_raw_parquet(spec_id)
        try:
            assert table.num_rows > 0, f"{spec_id}: raw parquet has 0 rows"

            missing = EXPECTED_COLUMNS - set(table.column_names)
            assert not missing, f"{spec_id}: raw parquet is missing columns {sorted(missing)}"

            for column in ("series_key", "value", "time_period", "period_start", "dataflow"):
                nulls = table.column(column).null_count
                assert nulls == 0, f"{spec_id}: {nulls} null values in {column!r}"

            # The asset must hold exactly the dataflow its spec id names; a mismatch
            # means a flowRef was fetched into the wrong asset.
            expected_flow = spec_id.removeprefix("bundesbank-").upper()
            flows = set(_strings(table, "dataflow").unique().to_pylist())
            assert flows == {expected_flow}, (
                f"{spec_id}: expected dataflow {expected_flow!r}, found {sorted(flows)}"
            )
        finally:
            del table


def test_zero_and_missing_sentinels_stay_distinct(spec_ids):
    """`-` is "Nichts vorhanden" (exactly zero); `.` is a missing or suppressed
    observation. Conflating them would either delete real zeros or invent them.

    Two invariants pin the distinction from opposite sides: every row the source
    flagged as an exact zero must hold 0.0, and no row flagged as *absent* may
    survive at all -- those cells are dropped in the fetch fn.
    """
    for spec_id in spec_ids:
        table = load_raw_parquet(spec_id)
        try:
            flag = _strings(table, "flag")
            value = table.column("value")

            zero_flagged = pc.fill_null(pc.equal(flag, FLAG_EXACT_ZERO), False)
            nonzero = pc.fill_null(pc.not_equal(value, 0.0), True)
            leaked = pc.sum(pc.and_(zero_flagged, nonzero)).as_py() or 0
            assert leaked == 0, (
                f"{spec_id}: {leaked} rows flagged {FLAG_EXACT_ZERO!r} carry a non-zero value "
                "- the '-' sentinel is no longer being read as an exact zero"
            )

            for absent_flag in FLAGS_MEANING_ABSENT:
                present = pc.sum(pc.fill_null(pc.equal(flag, absent_flag), False)).as_py() or 0
                assert present == 0, (
                    f"{spec_id}: {present} rows flagged {absent_flag!r} were materialised "
                    "- a missing observation was read as a real value"
                )

            nans = pc.sum(pc.is_nan(value)).as_py() or 0
            assert nans == 0, f"{spec_id}: {nans} NaN values in the observations"
        finally:
            del table
