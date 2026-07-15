-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Temporal series table; confirm aggregation dimensions before summing across categories.
SELECT
    "year",
    "alone",
    "with_spouse_and_children",
    "with_children",
    "with_spouse",
    "with_relatives_or_friends",
    "institutions_eg_hospital",
    "homeless",
    "total"
FROM "sg-data-d-2194c996aec35fe9e9289942ea88343e"
