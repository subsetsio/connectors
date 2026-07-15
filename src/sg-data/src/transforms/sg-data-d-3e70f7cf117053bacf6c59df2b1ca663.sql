-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "mother_ethnic_group",
    "place_of_occurrence",
    "attendant_at_birth",
    "child_gender",
    "still_births_count"
FROM "sg-data-d-3e70f7cf117053bacf6c59df2b1ca663"
