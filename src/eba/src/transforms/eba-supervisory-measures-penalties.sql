-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: CRD and IFD frameworks have different measure and penalty universes; compare or aggregate within a framework unless intentionally combining them.
SELECT
    "framework",
    "reporting_year",
    "competent_authority",
    "item_code",
    "category",
    "item_label",
    "count"
FROM "eba-supervisory-measures-penalties"
