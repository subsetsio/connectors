"""Health-invariant tests for SIAP raw downloads."""

from subsets_utils import load_raw_parquet


EXPECTED_COLUMNS = {
    "siap-agricola-municipal": {"source_year", "anio", "idmunicipio", "idcultivo", "volumenproduccion"},
    "siap-agricola-nacional": {"source_year", "anio", "idcultivo", "volumenproduccion"},
    "siap-pecuario-municipal": {"source_year", "anio", "cvempio", "cveproducto", "volumen"},
    "siap-pecuario-nacional": {"source_year", "anio", "cveproducto", "volumen"},
}


def test_all_raw_assets_nonempty(spec_ids):
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert table.num_rows > 0, f"{sid}: raw parquet has 0 rows"


def test_expected_columns_present(spec_ids):
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        cols = set(table.column_names)
        missing = EXPECTED_COLUMNS[sid] - cols
        assert not missing, f"{sid}: missing columns {sorted(missing)}"


def test_years_are_populated(spec_ids):
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        years = table.column("source_year")
        assert years.null_count == 0, f"{sid}: source_year contains nulls"
        assert len(set(years.to_pylist())) >= 18, f"{sid}: unexpectedly few years"
