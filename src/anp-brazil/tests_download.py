"""Post-DAG health invariants for ANP Brazil raw assets.

These run in-connector after the download nodes, loading raw through the same
subsets_utils loader the fetch fn used (all-string Parquet). They catch silent
degradation that file-existence alone misses: empty payloads, lost header,
wrong encoding/delimiter collapsing everything into one column.
"""
from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every ANP subset publishes a full history; an empty raw asset means the
    landing page changed, the file 404'd, or parsing dropped every row."""
    for sid in spec_ids:
        t = load_raw_parquet(sid)
        assert t.num_rows > 0, f"{sid}: raw parquet has 0 rows"


def test_multi_column_schema(spec_ids):
    """Each ANP CSV has several `;`-delimited columns. A single-column raw table
    means the delimiter/encoding sniff failed and the row collapsed to one field."""
    for sid in spec_ids:
        t = load_raw_parquet(sid)
        assert t.num_columns >= 2, (
            f"{sid}: only {t.num_columns} column(s) -> delimiter/encoding parse broke"
        )


def test_period_column_present(spec_ids):
    """Every subset carries a period/key column (ano, periodo, mes_ano, or
    data_da_coleta). Its absence means the header row was mis-read."""
    period_cols = {"ano", "periodo", "mes_ano", "data_da_coleta"}
    for sid in spec_ids:
        cols = set(load_raw_parquet(sid).column_names)
        assert cols & period_cols, f"{sid}: no period column among {sorted(cols)}"
