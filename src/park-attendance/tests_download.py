from subsets_utils import load_raw_parquet


def test_parks_directory_populated():
    """parks.json should enumerate ~131 parks across many countries; a big drop
    means the JSON shape changed or the fetch degraded."""
    t = load_raw_parquet("park-attendance-parks")
    assert len(t) >= 100, f"parks: only {len(t)} rows; expected >=100"
    countries = set(t.column("country").to_pylist())
    assert len(countries) >= 10, f"parks: only {len(countries)} countries"
    ids = t.column("park_id").to_pylist()
    assert len(ids) == len(set(ids)), "parks: duplicate park_id in directory"


def test_attendance_nonempty_and_sane():
    """Attendance scrape should yield thousands of (park, year) rows with
    plausible years and positive counts."""
    t = load_raw_parquet("park-attendance-attendance")
    assert len(t) >= 500, f"attendance: only {len(t)} rows; expected >=500"

    years = t.column("year").to_pylist()
    assert min(years) >= 1950, f"attendance: implausible min year {min(years)}"
    assert max(years) <= 2100, f"attendance: implausible max year {max(years)}"

    counts = t.column("annual_attendance").to_pylist()
    assert all(c > 0 for c in counts), "attendance: non-positive attendance present"

    # Multiple parks should contribute, not just one.
    parks = set(t.column("park_id").to_pylist())
    assert len(parks) >= 30, f"attendance: only {len(parks)} parks have data"
