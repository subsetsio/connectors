-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "election_code",
    "chamber",
    "election_date",
    "election_title"
FROM "inter-parliamentary-union-elections"
