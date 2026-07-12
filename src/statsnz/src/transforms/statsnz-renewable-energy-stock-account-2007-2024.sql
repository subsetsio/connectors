-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("year" AS BIGINT) AS year,
    "resource",
    "variable",
    "units",
    "magnitude",
    "source",
    "data_value",
    "flag"
FROM "statsnz-renewable-energy-stock-account-2007-2024"
