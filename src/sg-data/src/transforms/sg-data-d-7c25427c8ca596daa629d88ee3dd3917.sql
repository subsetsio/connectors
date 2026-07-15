-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Temporal series table; confirm aggregation dimensions before summing across categories.
SELECT
    "period",
    "region",
    "cor",
    "leisure",
    "holiday",
    "vfr",
    "business",
    "general_business_purpose",
    "mice",
    "others",
    "not_stated"
FROM "sg-data-d-7c25427c8ca596daa629d88ee3dd3917"
