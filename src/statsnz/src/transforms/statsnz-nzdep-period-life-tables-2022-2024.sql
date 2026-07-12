-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "measure",
    "quantile",
    "NZDep2023" AS nzdep2023,
    "time",
    "sex",
    "age",
    CAST("value" AS DOUBLE) AS value,
    "area",
    "geography",
    CAST("value_rnd" AS DOUBLE) AS value_rnd
FROM "statsnz-nzdep-period-life-tables-2022-2024"
