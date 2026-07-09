-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "value",
    CAST("sample_size" AS BIGINT) AS sample_size,
    CAST("calendar_years" AS BIGINT) AS calendar_years,
    CAST("time" AS BIGINT) AS time,
    "countries",
    "geography",
    "sex",
    "sex_1",
    "wellbeing_estimate",
    "estimate",
    "measure_of_wellbeing",
    "measureofwellbeing"
FROM "ons-childrens-wellbeing"
