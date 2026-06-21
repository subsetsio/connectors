"""Health invariants for the data-gov download stage.

datasets and resources are written as per-page ndjson batches
(`<asset>-<page>`); organizations is a single ndjson asset. We load raw through
subsets_utils so the checks behave identically locally and in the cloud.
"""

from subsets_utils import load_raw_ndjson
from subsets_utils.io import list_raw_files


def _asset_id(rel_path: str) -> str:
    """Strip dir + ndjson(.zst/.gz) suffix from a list_raw_files path."""
    name = rel_path.split("/")[-1]
    for suffix in (".ndjson.zst", ".ndjson.gz", ".ndjson"):
        if name.endswith(suffix):
            return name[: -len(suffix)]
    return name


def test_datasets_batches_nonempty():
    """The dataset corpus crawl should produce many batches, each with rows."""
    batches = list_raw_files("data-gov-datasets-*")
    assert len(batches) > 100, f"expected hundreds of dataset batches, got {len(batches)}"
    rows = load_raw_ndjson(_asset_id(sorted(batches)[0]))
    assert rows, "first dataset batch is empty"
    r = rows[0]
    assert r.get("id"), "dataset row missing id"
    for col in ("name", "title", "metadata_modified", "organization"):
        assert col in r, f"dataset row missing column {col}"


def test_resources_batches_nonempty():
    """Resource inventory should produce batches with file-level rows."""
    batches = list_raw_files("data-gov-resources-*")
    assert len(batches) > 50, f"expected many resource batches, got {len(batches)}"
    rows = load_raw_ndjson(_asset_id(sorted(batches)[0]))
    assert rows, "first resource batch is empty"
    r = rows[0]
    assert r.get("id"), "resource row missing id"
    for col in ("package_id", "format", "url"):
        assert col in r, f"resource row missing column {col}"


def test_organizations_nonempty():
    """All 132 publishing orgs should be captured with package counts."""
    rows = load_raw_ndjson("data-gov-organizations")
    assert len(rows) > 100, f"expected ~132 organizations, got {len(rows)}"
    r = rows[0]
    for col in ("name", "package_count", "organization_type"):
        assert col in r, f"organization row missing column {col}"
