-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Deficiency Prefix" AS deficiency_prefix,
    "Deficiency Tag Number" AS deficiency_tag_number,
    "Deficiency Prefix and Number" AS deficiency_prefix_and_number,
    "Deficiency Description" AS deficiency_description,
    "Deficiency Category" AS deficiency_category
FROM "cms-tagd-9999"
