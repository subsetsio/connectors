-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "election_result",
    "presidential_approval",
    "poll_average"
FROM "fivethirtyeight-early-senate-polls-early-senate-polls"
