"""Health invariants for ENTSOG raw assets, run post-DAG inside the connector."""
from subsets_utils import load_raw_ndjson, list_raw_files

# entities pulled as a single full-corpus ndjson asset (asset id == spec id)
FULL_SPECS = {
    "entsog-operators",
    "entsog-operatorpointdirections",
    "entsog-connectionpoints",
    "entsog-interconnections",
    "entsog-urgentmarketmessages",
    "entsog-tariffssimulations",
    "entsog-tariffsfulls",
}
# date-batched time-series — raw lands in many <spec>-<bucket>-pN batch files
TS_SPECS = {
    "entsog-operationaldata",
    "entsog-interruptions",
    "entsog-cmpunavailables",
    "entsog-cmpunsuccessfulrequests",
    "entsog-cmpauctions",
}


def test_full_assets_nonempty(spec_ids):
    """Each full-corpus endpoint must yield rows; an empty payload means the
    endpoint changed shape or the sweep broke after page 0."""
    for sid in spec_ids:
        if sid not in FULL_SPECS:
            continue
        rows = load_raw_ndjson(sid)
        assert rows and len(rows) > 0, f"{sid}: full-corpus ndjson is empty"


def test_full_assets_have_id(spec_ids):
    """Records must carry the source `id` the transforms key/dedup on."""
    for sid in spec_ids:
        if sid not in FULL_SPECS:
            continue
        rows = load_raw_ndjson(sid)
        sample = rows[: min(50, len(rows))]
        missing = [r for r in sample if not r.get("id")]
        assert not missing, f"{sid}: {len(missing)}/{len(sample)} sampled rows lack `id`"


def test_timeseries_have_batches(spec_ids):
    """Each time-series spec must have produced at least one raw batch file and
    those batches must hold rows; zero means the date-window backfill silently
    fetched nothing (archive boundary moved, params drifted)."""
    for sid in spec_ids:
        if sid not in TS_SPECS:
            continue
        batches = list_raw_files(f"{sid}-*")
        assert batches, f"{sid}: no date-window batch files produced"
        # the batch asset id is the filename minus its compression/format suffix
        first = batches[0].split(".")[0]
        rows = load_raw_ndjson(first)
        assert rows and len(rows) > 0, f"{sid}: first batch {first} is empty"
