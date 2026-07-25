-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    CAST("total" AS BIGINT) AS total,
    CAST("large_regional_carriers" AS BIGINT) AS large_regional_carriers,
    CAST("national_carriers" AS BIGINT) AS national_carriers,
    CAST("major_carriers" AS BIGINT) AS major_carriers
FROM "u-s-department-of-transportation-33xp-y9fx"
