import csv
from io import StringIO

from subsets_utils import load_raw_file


def test_csv_assets_have_rows(spec_ids):
    for spec_id in spec_ids:
        text = load_raw_file(spec_id, extension="csv")
        rows = list(csv.reader(StringIO(text)))
        assert len(rows) >= 2, f"{spec_id}: csv has no data rows"
        assert len(rows[0]) >= 2, f"{spec_id}: csv header has fewer than two columns"


def test_csv_headers_are_not_blank(spec_ids):
    for spec_id in spec_ids:
        text = load_raw_file(spec_id, extension="csv")
        header = next(csv.reader(StringIO(text)))
        blanks = [idx for idx, value in enumerate(header) if not value.strip()]
        assert not blanks, f"{spec_id}: blank header columns at positions {blanks}"
