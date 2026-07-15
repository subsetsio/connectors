-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "no_of_pl_cw_cases",
    "no_of_or_cw_cases",
    "total_no_of_cw_cases"
FROM "sg-data-d-5fa01efe9171c5b300f3c44c07abb3b2"
