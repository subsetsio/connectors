-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Title" AS title,
    "Date" AS date,
    "Federal Reporter Citation" AS federal_reporter_citation,
    "Westlaw Citation" AS westlaw_citation,
    "Issue" AS issue,
    "Weight" AS weight,
    "Judge1" AS judge1,
    "Judge2" AS judge2,
    "Judge3" AS judge3,
    "Vote1" AS vote1,
    "Vote2" AS vote2,
    "Vote3" AS vote3,
    "Category" AS category
FROM "fivethirtyeight-tenth-circuit-tenth-circuit"
