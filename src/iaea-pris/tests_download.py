"""Post-DAG health invariants for the IAEA PRIS raw assets.

These catch silent degradation that file-existence alone misses — an empty
scrape (TLS/cipher regression, layout change), a truncated id walk, or a parse
that quietly yields all-null columns.
"""

from subsets_utils import load_raw_parquet


def test_reactors_nonempty(spec_ids):
    """The reactor specification scrape should yield hundreds of reactors
    (~720 observed). A tiny count means the id walk stopped early or the spec
    spans moved."""
    if "iaea-pris-reactors" not in spec_ids:
        return
    t = load_raw_parquet("iaea-pris-reactors")
    assert t.num_rows >= 600, f"iaea-pris-reactors: only {t.num_rows} reactors (expected ~720)"
    names = t.column("name").to_pylist()
    nonnull = [n for n in names if n]
    assert len(nonnull) >= 600, f"iaea-pris-reactors: {len(nonnull)} non-null names; parsing likely broke"


def test_reactor_ids_unique(spec_ids):
    if "iaea-pris-reactors" not in spec_ids:
        return
    ids = load_raw_parquet("iaea-pris-reactors").column("reactor_id").to_pylist()
    assert len(ids) == len(set(ids)), "iaea-pris-reactors: duplicate reactor_id — id walk revisited pages"


def test_performance_nonempty(spec_ids):
    """Annual performance should be thousands of (reactor, year) rows spanning
    decades. Few rows means the performance table parser missed the layout."""
    if "iaea-pris-performance" not in spec_ids:
        return
    t = load_raw_parquet("iaea-pris-performance")
    assert t.num_rows >= 8000, f"iaea-pris-performance: only {t.num_rows} rows (expected >10k)"
    years = [y for y in t.column("year").to_pylist() if y is not None]
    assert years, "iaea-pris-performance: no parsed years"
    assert min(years) <= 1980, f"iaea-pris-performance: earliest year {min(years)} too recent; history truncated"
    elec = [e for e in t.column("electricity_supplied_gwh").to_pylist() if e is not None]
    assert len(elec) >= 5000, f"iaea-pris-performance: only {len(elec)} non-null generation values"
