-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: A country and indicator can have multiple categorical/text values from different NDC document contexts, and exact duplicate rows can appear in the upstream extract.
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
FROM "wri-ndc-content"
