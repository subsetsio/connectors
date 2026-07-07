from subsets_utils import load_raw_parquet


EXPECTED_COLUMNS = {
    "lok-dhaba-general-election-results": {
        "State_Name", "Assembly_No", "Constituency_No", "Year", "Candidate",
        "Party", "Votes", "Valid_Votes", "Electors", "Election_Type",
    },
    "lok-dhaba-assembly-election-results": {
        "State_Name", "Assembly_No", "Constituency_No", "Year", "Candidate",
        "Party", "Votes", "Age", "District_Name", "Election_Type",
    },
    "lok-dhaba-general-election-segment-results": {
        "State_Name", "Assembly_No", "Constituency_No", "Year", "PC_Name",
        "PC_No", "Candidate", "Party", "Votes", "Election_Type",
    },
}


def test_all_raw_assets_nonempty(spec_ids):
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert table.num_rows > 1000, f"{sid}: unexpectedly small raw table"


def test_expected_core_columns_present(spec_ids):
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        missing = EXPECTED_COLUMNS[sid] - set(table.schema.names)
        assert not missing, f"{sid}: missing expected columns {sorted(missing)}"


def test_election_type_populated(spec_ids):
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        values = table.column("Election_Type").drop_null().unique().to_pylist()
        assert values, f"{sid}: Election_Type is empty"
