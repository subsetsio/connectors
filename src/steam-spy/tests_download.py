"""Health-invariant tests for Steam Spy raw assets."""

from subsets_utils import load_raw_ndjson


def test_apps_raw_nonempty_and_shaped(spec_ids):
    assert spec_ids == ["steam-spy-apps"], f"unexpected download specs: {spec_ids}"
    rows = load_raw_ndjson("steam-spy-apps")
    assert len(rows) >= 10000, f"steam-spy-apps: only {len(rows)} rows; expected >= 10000"

    first = rows[0]
    required = {"appid", "name", "owners", "positive", "negative", "ccu", "source_page"}
    missing = required - set(first)
    assert not missing, f"steam-spy-apps: first row missing expected keys {sorted(missing)}"

    appids = [row.get("appid") for row in rows]
    assert len(appids) == len(set(appids)), "steam-spy-apps: duplicate appids in raw payload"
