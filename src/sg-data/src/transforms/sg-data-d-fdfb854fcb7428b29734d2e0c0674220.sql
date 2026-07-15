-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "constituency",
    "no_of_registered_electors",
    "no_of_rejected_votes",
    "no_of_spoilt_ballot_papers"
FROM "sg-data-d-fdfb854fcb7428b29734d2e0c0674220"
