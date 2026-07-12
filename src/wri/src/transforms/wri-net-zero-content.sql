-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Values are categorical or free text and may include source links or dates embedded in HTML/text rather than normalized fields.
SELECT
    "iso_code3",
    "country",
    "global_category",
    "overview_category",
    "sector",
    "subsector",
    "indicator_id",
    "value",
    "source",
    "indicator_name"
FROM "wri-net-zero-content"
