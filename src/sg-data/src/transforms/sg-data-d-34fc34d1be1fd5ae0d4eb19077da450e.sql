-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "quarter",
    "type_of_space",
    "provisional_permission",
    "written_permission",
    "building_plan_approval",
    "building_commencement",
    "building_completion"
FROM "sg-data-d-34fc34d1be1fd5ae0d4eb19077da450e"
