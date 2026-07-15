-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "type_of_institution",
    "number_of_institution"
FROM "sg-data-d-9a8697c5770bca5ffc1dffa320c2e24a"
