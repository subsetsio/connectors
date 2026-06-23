"""Post-DAG health invariants for the Global Volcanism Program connector.

These run in-connector after the download nodes, reading raw through the same
loader the fetch used (save_raw_ndjson -> load_raw_ndjson). They catch silent
degradation that file-existence alone misses: an empty/short payload (the WFS
edge switched to an XML exception, or paging broke after page 1) and a missing
core attribute (the layer schema changed underneath us).
"""
from subsets_utils import load_raw_ndjson

SLUG = "global-volcanism-program"

# Minimum feature counts we expect per layer, from the GVP catalog (~1.2-1.4k
# Holocene volcanoes, ~11k confirmed Holocene eruptions, a few hundred
# Pleistocene volcanoes). Loose floors: a real degradation drops to ~0/1 page.
_MIN_ROWS = {
    f"{SLUG}-smithsonian-votw-holocene-volcanoes": 1000,
    f"{SLUG}-smithsonian-votw-holocene-eruptions": 8000,
    f"{SLUG}-smithsonian-votw-pleistocene-volcanoes": 50,
}


def test_all_raw_assets_nonempty(spec_ids):
    """Every layer's raw asset must hold rows. Empty usually means the endpoint
    returned a WFS exception or auth/UA was silently rejected."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert len(rows) > 0, f"{sid}: raw ndjson has 0 rows"


def test_min_feature_counts(spec_ids):
    """Known layers should clear their catalog floor; a short pull means paging
    truncated or the server capped results."""
    for sid in spec_ids:
        floor = _MIN_ROWS.get(sid)
        if floor is None:
            continue
        n = len(load_raw_ndjson(sid))
        assert n >= floor, f"{sid}: got {n} features, expected >= {floor}"


def test_volcano_layers_have_core_columns(spec_ids):
    """Every VOTW volcano/eruption layer carries Volcano_Number + Volcano_Name;
    their absence means the layer's attribute schema changed."""
    for sid in spec_ids:
        if "emissions" in sid:
            continue
        rows = load_raw_ndjson(sid)
        if not rows:
            continue
        cols = set(rows[0].keys())
        missing = {"Volcano_Number", "Volcano_Name"} - cols
        assert not missing, f"{sid}: missing core columns {sorted(missing)} (have {sorted(cols)[:12]})"
