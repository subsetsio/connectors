-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "By type" AS by_type,
    strptime("monthly (by cumulative)", '%Y-%m')::DATE AS monthly_by_cumulative,
    "value",
    "unit"
FROM "nso-mongolia-dt-nso-2200-012v1-1"
