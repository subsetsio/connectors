"""Health invariants for the DVF download node.

The raw asset is written as a sequence of per-(year, department) parquet batches
named `dvf-transactions-<year>-<dept>`. We load those batch files back through
the subsets_utils loader and check the corpus is non-trivially populated and
carries its key columns — catching silent degradation (empty payloads,
truncated downloads, a format switch) that file existence alone misses.
"""

from subsets_utils import list_raw_files, load_raw_parquet

KEY_COLUMNS = {
    "id_mutation", "date_mutation", "valeur_fonciere",
    "code_departement", "type_local", "latitude", "longitude",
}


def _batch_assets():
    # Batch files are named dvf-transactions-<year>-<dept>.parquet
    names = set()
    for path in list_raw_files("dvf-transactions-*.parquet"):
        stem = path.rsplit("/", 1)[-1]
        names.add(stem[: -len(".parquet")])
    return sorted(names)


def test_batches_present_and_nonempty():
    assets = _batch_assets()
    assert len(assets) >= 200, f"expected >=200 (year x dept) batches, got {len(assets)}"
    total = 0
    for a in assets:
        tbl = load_raw_parquet(a)
        assert len(tbl) > 0, f"{a}: raw parquet has 0 rows"
        total += len(tbl)
    assert total >= 3_000_000, f"corpus has only {total} rows across {len(assets)} batches"


def test_schema_has_key_columns():
    assets = _batch_assets()
    assert assets, "no dvf-transactions batches found"
    cols = set(load_raw_parquet(assets[0]).column_names)
    missing = KEY_COLUMNS - cols
    assert not missing, f"raw missing key columns: {sorted(missing)}"


def test_valeur_fonciere_not_all_null():
    assets = _batch_assets()
    import pyarrow.compute as pc
    sample = load_raw_parquet(assets[0])
    nn = pc.sum(pc.is_valid(sample["valeur_fonciere"])).as_py()
    assert nn and nn > 0, f"{assets[0]}: valeur_fonciere is entirely null"
