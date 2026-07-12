-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "major_region",
    "employment_prospects",
    "weight",
    "quarter",
    "value",
    "cube_id",
    "updated"
FROM "federal-statistical-office-px-x-0602000000-106"
