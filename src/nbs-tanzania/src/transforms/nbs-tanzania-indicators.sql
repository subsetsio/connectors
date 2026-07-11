-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Indicator definitions are area-specific; join or filter on both `indicator_id` and `area` when using this as metadata for observations.
SELECT
    "indicator_id",
    "area",
    "description"
FROM "nbs-tanzania-indicators"
