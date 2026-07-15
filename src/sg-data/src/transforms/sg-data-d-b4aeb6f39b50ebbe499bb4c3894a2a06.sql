-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "scholarship_scheme",
    "no_of_psc_scholarships_awarded"
FROM "sg-data-d-b4aeb6f39b50ebbe499bb4c3894a2a06"
