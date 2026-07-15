-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "month",
    "birth_type",
    "mother_age_group",
    "total_number_of_mother"
FROM "sg-data-d-9904ead960a059fa235120dd2de114d8"
