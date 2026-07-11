-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Type of legal" AS type_of_legal,
    "Group of economic activity" AS group_of_economic_activity,
    "Quarter" AS quarter,
    "value",
    "unit"
FROM "nso-mongolia-dt-nso-2600-016v1"
