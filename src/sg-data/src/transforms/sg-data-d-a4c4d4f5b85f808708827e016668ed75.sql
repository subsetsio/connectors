-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "type_of_space",
    "provisional_permission",
    "written_permission",
    "building_plan_approval",
    "building_commencement",
    "building_completion"
FROM "sg-data-d-a4c4d4f5b85f808708827e016668ed75"
