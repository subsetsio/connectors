-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_resource",
    "source_file",
    "department",
    "Date" AS date,
    CAST("fiscal_year" AS BIGINT) AS fiscal_year,
    CAST("fiscal_year_period" AS BIGINT) AS fiscal_year_period,
    "Name" AS name,
    "Amount" AS amount,
    "Account" AS account
FROM "instituto-de-estad-sticas-de-puerto-rico-datos-del-sistema-de-transparencia-financiera-de-puerto-rico"
