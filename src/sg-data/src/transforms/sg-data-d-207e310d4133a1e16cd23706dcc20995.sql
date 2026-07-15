-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Temporal series table; confirm aggregation dimensions before summing across categories.
SELECT
    "period",
    "region",
    "cor",
    "alone",
    "spouse",
    "friends",
    "child_below_19yrs",
    "business",
    "parents_and_in_law",
    "siblings",
    "relatives",
    "partner",
    "child_above_19yrs",
    "average_family_size",
    "average_party_size"
FROM "sg-data-d-207e310d4133a1e16cd23706dcc20995"
