-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("year" AS BIGINT) AS year,
    "state",
    "area",
    "fclass",
    CAST("fatalities" AS BIGINT) AS fatalities
FROM "u-s-department-of-transportation-nxha-wg33"
