"""Post-DAG health invariants for the Banco Central do Brasil connector.

Catches silent degradation that mere file existence misses: empty entity sets,
a firehose that wrote zero batches, or a format switch that drops every row.
"""
from subsets_utils import list_raw_files, load_raw_ndjson

# Specs whose raw is a single ndjson asset written at exactly spec.id.
_SINGLE = {
    "banco-central-do-brasil-sgs-series",
}
# Firehose specs whose raw is one-or-more batch files named "<spec.id>-<batch>".
_FIREHOSE = {
    "banco-central-do-brasil-ptax-cotacaodolardia",
    "banco-central-do-brasil-ptax-cotacaomoedadia",
    "banco-central-do-brasil-ptax-cotacaomoedaaberturaouintermediario",
    "banco-central-do-brasil-ifdata-ifdatacadastro",
    "banco-central-do-brasil-ifdata-ifdatavalores",
    "banco-central-do-brasil-sgs-values",
}


def test_single_assets_nonempty(spec_ids):
    """Single-file ndjson assets (Expectativas, PTAX periodo, sgs-series) must
    hold rows — an empty set means the endpoint changed shape or auth lapsed."""
    for sid in spec_ids:
        if sid in _FIREHOSE:
            continue
        rows = load_raw_ndjson(sid)
        assert len(rows) > 0, f"{sid}: ndjson asset has 0 rows"


def test_firehose_assets_have_batches(spec_ids):
    """Firehose specs must have produced at least one batch file. Zero batches
    after a refresh means the watermark/discovery path is broken."""
    for sid in spec_ids:
        if sid not in _FIREHOSE:
            continue
        files = list_raw_files(f"{sid}-")
        assert files, f"{sid}: firehose produced no batch files"


def test_sgs_values_shape(spec_ids):
    """sgs-values batches must carry the (series_code, data, valor) triple."""
    sid = "banco-central-do-brasil-sgs-values"
    if sid not in spec_ids:
        return
    files = list_raw_files(f"{sid}-")
    if not files:
        return
    # Recover the first batch's asset id from its path, then load it.
    asset = files[0].split("/")[-1]
    for ext in (".ndjson.zst", ".ndjson.gz", ".ndjson"):
        if asset.endswith(ext):
            asset = asset[: -len(ext)]
            break
    rows = load_raw_ndjson(asset)
    if rows:
        assert {"series_code", "data", "valor"} <= set(rows[0]), \
            f"{sid}: batch row missing expected keys, got {list(rows[0])}"
