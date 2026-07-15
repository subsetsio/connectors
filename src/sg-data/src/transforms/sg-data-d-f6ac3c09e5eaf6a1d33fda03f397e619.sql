-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "no_of_registered_electors",
    "no_of_rejected_votes",
    "no_of_spoilt_ballot_papers"
FROM "sg-data-d-f6ac3c09e5eaf6a1d33fda03f397e619"
