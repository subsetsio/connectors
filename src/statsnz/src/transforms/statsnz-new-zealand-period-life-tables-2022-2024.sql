-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "measure",
    "quantile",
    "time",
    "sex",
    "age",
    CAST("value" AS DOUBLE) AS value,
    "ethnic"
FROM "statsnz-new-zealand-period-life-tables-2022-2024"
