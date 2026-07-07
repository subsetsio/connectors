from subsets_utils import load_raw_parquet


def test_reference_tables_nonempty(spec_ids):
    expected = {
        "reuters-institute-demographics": 10,
        "reuters-institute-markets": 50,
        "reuters-institute-questions": 70,
    }
    for spec_id, minimum in expected.items():
        table = load_raw_parquet(spec_id)
        assert len(table) >= minimum, (
            f"{spec_id}: only {len(table)} rows, expected at least {minimum}"
        )


def test_survey_observations_volume_and_columns(spec_ids):
    table = load_raw_parquet("reuters-institute-survey-observations")
    assert len(table) >= 400_000, (
        f"survey observations: only {len(table)} rows, expected >=400,000"
    )
    for column_name in ("question_id", "year", "country_code", "option_id", "pct"):
        column = table.column(column_name)
        assert column.null_count == 0, f"survey observations: null {column_name}"


def test_current_question_universe_present(spec_ids):
    table = load_raw_parquet("reuters-institute-survey-observations")
    question_count = len(set(table.column("question_id").to_pylist()))
    assert question_count >= 11, (
        f"survey observations: only {question_count} question groups"
    )
