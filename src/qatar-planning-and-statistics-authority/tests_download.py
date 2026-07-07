import csv
import io

from subsets_utils import load_raw_file


def test_all_csv_assets_have_header_and_rows(spec_ids):
    for spec_id in spec_ids:
        content = load_raw_file(spec_id, extension="csv", binary=True)
        text = content.decode("utf-8-sig")
        reader = csv.reader(io.StringIO(text))
        try:
            header = next(reader)
        except StopIteration:
            raise AssertionError(f"{spec_id}: CSV is empty")
        assert len([col for col in header if col]) >= 1, f"{spec_id}: CSV header has no named columns"
        first_row = next(reader, None)
        assert first_row is not None, f"{spec_id}: CSV has a header but no data rows"
