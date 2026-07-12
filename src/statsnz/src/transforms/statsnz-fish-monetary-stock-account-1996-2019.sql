-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "species",
    CAST("year" AS BIGINT) AS year,
    "variable",
    "units",
    "magnitude",
    "source",
    "data_value",
    "flag"
FROM "statsnz-fish-monetary-stock-account-1996-2019"
