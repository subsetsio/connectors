-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("year" AS BIGINT) AS year,
    "Industry_code" AS industry_code,
    "Industry_desc" AS industry_desc,
    "Environmental_base" AS environmental_base,
    "National_accounts_var" AS national_accounts_var,
    "units",
    "magnitude",
    "source",
    CAST("data_value" AS BIGINT) AS data_value,
    "flag"
FROM "statsnz-environmental-tax-account-1999-2024"
