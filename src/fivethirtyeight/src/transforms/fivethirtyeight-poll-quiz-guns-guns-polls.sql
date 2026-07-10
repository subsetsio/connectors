-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Question" AS question,
    "Start" AS start,
    "End" AS end,
    "Pollster" AS pollster,
    "Population" AS population,
    "Support" AS support,
    "Republican Support" AS republican_support,
    "Democratic Support" AS democratic_support,
    "URL" AS url
FROM "fivethirtyeight-poll-quiz-guns-guns-polls"
