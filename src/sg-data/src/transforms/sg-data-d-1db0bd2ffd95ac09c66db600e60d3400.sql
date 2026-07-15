-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Temporal series table; confirm aggregation dimensions before summing across categories.
SELECT
    "period",
    "max",
    "paid",
    "available",
    "occupied",
    "aor",
    "rm_revenue",
    "arr",
    "revpar"
FROM "sg-data-d-1db0bd2ffd95ac09c66db600e60d3400"
