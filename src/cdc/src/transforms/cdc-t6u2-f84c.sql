-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "GEOID" AS geoid,
    "Intent" AS intent,
    "Period" AS period,
    CAST("Count" AS BIGINT) AS count,
    CAST("Rate" AS DOUBLE) AS rate,
    "Type" AS type,
    strptime("Data_As_Of", '%m/%d/%Y')::DATE AS data_as_of,
    "TTM_Date_Range" AS ttm_date_range
FROM "cdc-t6u2-f84c"
