"""Post-download health checks for TED procurement notices."""

from datetime import date

from subsets_utils import load_raw_ndjson


def test_notice_asset_nonempty(spec_ids):
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert rows, f"{sid}: no notice rows parsed from the daily XML package"


def test_notice_rows_have_core_identifiers(spec_ids):
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        missing = [
            idx
            for idx, row in enumerate(rows[:100])
            if not row.get("publication_number") or not row.get("package_issue_token")
        ]
        assert not missing, f"{sid}: rows missing core identifiers in first 100: {missing}"


def test_package_publication_date_recent(spec_ids):
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        latest = max(date.fromisoformat(row["package_publication_date"]) for row in rows)
        age_days = (date.today() - latest).days
        assert age_days <= 14, f"{sid}: latest package is {age_days} days old"
