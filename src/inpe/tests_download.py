"""Health-invariant tests — run post-DAG, in-connector, against the raw assets
the download nodes wrote (loaded through subsets_utils, same as production)."""
from subsets_utils import load_raw_parquet

EXPECTED_COLUMNS = {
    "inpe-focos-brasil-estado-mensal": {"ano", "mes", "estado", "n_focos"},
    "inpe-focos-brasil-bioma-mensal": {"ano", "mes", "bioma", "n_focos"},
    "inpe-focos-brasil-municipio-anual": {"ano", "estado", "municipio", "n_focos"},
    "inpe-focos-brasil-mensal": {
        "ano",
        "mes",
        "n_focos",
        "frp_medio",
        "risco_fogo_medio",
        "precipitacao_media",
        "dias_sem_chuva_medio",
    },
    "inpe-focos-america-sul-pais-mensal": {"ano", "mes", "pais", "n_focos"},
}


def test_all_raw_assets_nonempty(spec_ids):
    """A focos aggregate with zero rows means the directory listing broke or the
    zip schema changed and every row was filtered out."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_expected_columns_present(spec_ids):
    """The aggregation columns must be present — a missing column means the
    source CSV header changed and a field silently fell through as None."""
    for sid in spec_ids:
        cols = set(load_raw_parquet(sid).column_names)
        want = EXPECTED_COLUMNS.get(sid, set())
        missing = want - cols
        assert not missing, f"{sid}: missing columns {sorted(missing)} (have {sorted(cols)})"


def test_counts_are_positive(spec_ids):
    """Every aggregated row should carry a positive detection count; a zero or
    negative count would mean the GROUP BY emitted spurious empty groups."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        if "n_focos" not in table.column_names:
            continue
        import pyarrow.compute as pc

        bad = pc.sum(pc.less_equal(table["n_focos"], 0)).as_py() or 0
        assert bad == 0, f"{sid}: {bad} rows with non-positive n_focos"
