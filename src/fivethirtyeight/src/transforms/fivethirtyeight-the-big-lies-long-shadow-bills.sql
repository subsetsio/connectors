-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "State" AS state,
    "Bill" AS bill,
    "Introducing Party" AS introducing_party,
    "Category" AS category,
    "Status" AS status
FROM "fivethirtyeight-the-big-lies-long-shadow-bills"
