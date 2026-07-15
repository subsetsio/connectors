-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "level_of_school",
    "school_type",
    "number_of_pre_university_sch"
FROM "sg-data-d-190a5d7d5a612705bf13bb4cc37fc34e"
