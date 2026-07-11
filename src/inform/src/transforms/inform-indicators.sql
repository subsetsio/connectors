-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "indicator_id",
    "indicator_type",
    "indicator_description",
    "indicator_note",
    "provider",
    "default_weight",
    "missing_value",
    "unit",
    "indicator_group",
    "note",
    "link"
FROM "inform-indicators"
