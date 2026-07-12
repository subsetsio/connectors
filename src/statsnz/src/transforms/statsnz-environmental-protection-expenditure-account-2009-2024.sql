-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("year" AS BIGINT) AS year,
    "sector",
    "class",
    "cfn_tle1",
    "cfn_tle2",
    "units",
    "magnitude",
    "source",
    CAST("data_value" AS DOUBLE) AS data_value,
    "flag"
FROM "statsnz-environmental-protection-expenditure-account-2009-2024"
