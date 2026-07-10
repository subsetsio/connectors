-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "congress",
    "start_date",
    "chamber",
    "state_abbrev",
    "party_code",
    "bioname",
    "bioguide_id",
    "birthday",
    "cmltv_cong",
    "cmltv_chamber",
    "age_days",
    "age_years",
    "generation"
FROM "fivethirtyeight-congress-demographics-data-aging-congress"
