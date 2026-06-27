"""Health-invariant checks for the Journey North raw download.

The download writes one raw parquet batch per (map, year) under the asset id
prefix `journey-north-sightings-`. These tests catch silent degradation that
file existence alone would miss — a collapsed slug set, empty payloads, or a
format switch.
"""

from subsets_utils import list_raw_files, load_raw_parquet


def _batches(sid):
    return sorted(list_raw_files(f"{sid}-*.parquet"))


def test_many_batches_written(spec_ids):
    """Expect many (map, year) batches — ~34 maps over ~30 years. A handful
    means slug enumeration or year iteration broke."""
    for sid in spec_ids:
        files = _batches(sid)
        assert len(files) >= 50, f"{sid}: only {len(files)} raw batches; expected many (maps x years)"


def test_batches_cover_many_maps(spec_ids):
    """The batch filenames should span the bulk of the map taxonomy, not one
    or two layers."""
    for sid in spec_ids:
        files = _batches(sid)
        maps = set()
        for rel in files:
            stem = rel.rsplit("/", 1)[-1][: -len(".parquet")]
            # stem == journey-north-sightings-<map_slug>-<year>; strip prefix + trailing year
            tail = stem[len(sid) + 1:]
            maps.add(tail.rsplit("-", 1)[0])
        assert len(maps) >= 20, f"{sid}: batches cover only {len(maps)} map layers; expected >=20"


def test_batches_nonempty_and_typed(spec_ids):
    """Sample a few batches and confirm they hold rows with the expected key
    columns — empty payloads usually mean the endpoint changed shape."""
    for sid in spec_ids:
        files = _batches(sid)
        assert files, f"{sid}: no raw batch files found"
        sample = files[:: max(1, len(files) // 5)][:5]
        for rel in sample:
            asset = rel.rsplit("/", 1)[-1][: -len(".parquet")]
            table = load_raw_parquet(asset)
            assert len(table) > 0, f"{asset}: raw parquet has 0 rows"
            for col in ("sighting_id", "map_slug", "latitude", "longitude"):
                assert col in table.column_names, f"{asset}: missing column {col}"
