-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "GEOID" AS geoid,
    "NAME" AS name,
    "Intent" AS intent,
    "Period" AS period,
    "Count" AS count,
    CAST("Rate" AS DOUBLE) AS rate,
    strptime("Data_As_Of", '%m/%d/%Y')::DATE AS data_as_of,
    "TTM_Date_Range" AS ttm_date_range
FROM "cdc-fpsi-y8tj"
