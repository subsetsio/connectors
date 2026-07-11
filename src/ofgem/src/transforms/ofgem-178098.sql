-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The source chart rows do not have a scan-verified unique category or category-series key; treat rows as chart observations rather than aggregating by label alone.
SELECT
    "category",
    "series",
    "value"
FROM "ofgem-178098"
