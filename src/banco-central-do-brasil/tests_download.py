"""Post-DAG health invariants for the Banco Central do Brasil connector.

Catches silent degradation that mere file existence misses: empty entity sets,
a firehose that wrote zero batches, or a format switch that drops every row.
"""
from subsets_utils import list_raw_fragments, load_raw_ndjson

# Specs whose raw is a single ndjson asset written at exactly spec.id.
_SINGLE = {
    "banco-central-do-brasil-expectativas-expectativamercadomensais",
    "banco-central-do-brasil-expectativas-expectativamercadotop5trimestral",
    "banco-central-do-brasil-expectativas-expectativasmercadoanuais",
    "banco-central-do-brasil-expectativas-expectativasmercadoinflacao12meses",
    "banco-central-do-brasil-expectativas-expectativasmercadoinflacao24meses",
    "banco-central-do-brasil-expectativas-expectativasmercadoselic",
    "banco-central-do-brasil-expectativas-expectativasmercadotop5anuais",
    "banco-central-do-brasil-expectativas-expectativasmercadotop5inflacao12meses",
    "banco-central-do-brasil-expectativas-expectativasmercadotop5inflacao24meses",
    "banco-central-do-brasil-expectativas-expectativasmercadotop5mensais",
    "banco-central-do-brasil-expectativas-expectativasmercadotop5selic",
    "banco-central-do-brasil-expectativas-expectativasmercadotrimestrais",
    "banco-central-do-brasil-ptax-cotacaodolarperiodo",
    "banco-central-do-brasil-ptax-cotacaomoedaperiodo",
    "banco-central-do-brasil-sgs-series",
}
# Firehose specs whose raw is one-or-more batch files named "<spec.id>-<batch>".
_FIREHOSE = {
    "banco-central-do-brasil-ifdata-ifdatacadastro",
    "banco-central-do-brasil-ifdata-ifdatavalores",
    "banco-central-do-brasil-sgs-values",
}


def test_single_assets_nonempty(spec_ids):
    """Single-file ndjson assets (Expectativas, PTAX periodo, sgs-series) must
    hold rows — an empty set means the endpoint changed shape or auth lapsed."""
    for sid in spec_ids:
        if sid not in _SINGLE:
            continue
        rows = load_raw_ndjson(sid)
        assert len(rows) > 0, f"{sid}: ndjson asset has 0 rows"


def test_firehose_assets_have_batches(spec_ids):
    """Firehose specs must have committed at least one manifest fragment."""
    for sid in spec_ids:
        if sid not in _FIREHOSE:
            continue
        fragments = list_raw_fragments(sid, "ndjson.zst")
        assert fragments, f"{sid}: firehose produced no committed fragments"


def test_sgs_values_shape(spec_ids):
    """sgs-values batches must carry the (series_code, data, valor) triple."""
    sid = "banco-central-do-brasil-sgs-values"
    if sid not in spec_ids:
        return
    fragments = list_raw_fragments(sid, "ndjson.zst")
    if not fragments:
        return
    frag = sorted(fragments)[0]
    asset = f"{sid}-{frag}"
    rows = load_raw_ndjson(asset)
    if rows:
        assert {"series_code", "data", "valor"} <= set(rows[0]), \
            f"{sid}: batch row missing expected keys, got {list(rows[0])}"
