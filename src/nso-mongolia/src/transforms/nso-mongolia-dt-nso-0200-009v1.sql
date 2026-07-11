-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "National total" AS national_total,
    "Years of service" AS years_of_service,
    "Total" AS total,
    CAST("Years" AS BIGINT) AS years,
    "value",
    "unit"
FROM "nso-mongolia-dt-nso-0200-009v1"
