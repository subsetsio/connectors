-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "measure",
    "quantile",
    "area",
    "time",
    "sex",
    "age",
    "geography",
    "ethnic",
    CAST("value" AS DOUBLE) AS value
FROM "statsnz-subnational-period-life-tables-2022-2024"
