-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows mix national, regional, demographic, and other disaggregation categories in one column; filter `disaggregation` before aggregating observations.
SELECT
    "indicator_id",
    "area",
    "year",
    CAST("value" AS DOUBLE) AS "value",
    "unit",
    "disaggregation"
FROM "nbs-tanzania-values"
