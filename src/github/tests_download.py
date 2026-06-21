import json

from subsets_utils import raw_reader


def _count_and_first(asset):
    """Stream-count rows (bounded memory) and capture the first record."""
    n = 0
    first = None
    with raw_reader(asset, "ndjson.gz", mode="rt", compression="gzip") as f:
        for line in f:
            if not line.strip():
                continue
            if first is None:
                first = json.loads(line)
            n += 1
    return n, first


def test_advisories_corpus_complete(spec_ids):
    """The OSV corpus is ~290k advisories (github-reviewed + unreviewed CVE
    mirrors). <50k means the unreviewed tree was skipped or the archive parse
    truncated."""
    n, first = _count_and_first("github-advisories")
    assert n > 50000, f"github-advisories: {n} rows, expected >50000 (truncated parse?)"
    assert first is not None
    for key in ("ghsa_id", "severity", "published_at", "github_reviewed", "source_directory"):
        assert key in first, f"github-advisories: missing field {key!r}"
    assert first["ghsa_id"], "github-advisories: empty ghsa_id on first row"


def test_affected_packages_present(spec_ids):
    """Affected-package rows are the long-format companion; most advisories
    name >=1 affected package, so this should outnumber a tiny floor easily."""
    n, first = _count_and_first("github-affected")
    assert n > 50000, f"github-affected: {n} rows, expected >50000"
    assert first is not None
    for key in ("ghsa_id", "ecosystem", "package_name"):
        assert key in first, f"github-affected: missing field {key!r}"
    assert first["ecosystem"] and first["package_name"]
