-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "average_no_of_inmates_engaged_in_work_programmes"
FROM "sg-data-d-606eb23fb872a2363e01d86a978f687e"
