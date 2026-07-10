-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "question",
    "category",
    "yes",
    "no",
    "pollster",
    "dates",
    "link",
    "net"
FROM "fivethirtyeight-trump-2-poll-issue-questions-trump-poll-issue-questions"
