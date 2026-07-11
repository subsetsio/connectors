-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows include demographic split aggregates as well as all-respondent totals; filter split variables before aggregating results across demographic groups.
SELECT
    "question_id",
    "year",
    "country_code",
    "option_id",
    "split_var",
    "split_value",
    "pct",
    "base_unwt_calc"
FROM "reuters-institute-survey-observations"
