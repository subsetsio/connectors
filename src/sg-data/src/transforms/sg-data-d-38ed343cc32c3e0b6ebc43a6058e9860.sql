-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "provisional_permission",
    "written_permission",
    "building_plan_approval",
    "building_commencement",
    "building_completion"
FROM "sg-data-d-38ed343cc32c3e0b6ebc43a6058e9860"
