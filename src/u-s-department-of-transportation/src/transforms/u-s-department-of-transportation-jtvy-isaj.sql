-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    CAST("total" AS DOUBLE) AS total,
    CAST("large_regional_carriers" AS DOUBLE) AS large_regional_carriers,
    CAST("national_carriers" AS DOUBLE) AS national_carriers,
    CAST("major_carriers" AS DOUBLE) AS major_carriers
FROM "u-s-department-of-transportation-jtvy-isaj"
