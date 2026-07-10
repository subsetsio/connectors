-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Person" AS person,
    "Party" AS party,
    "State" AS state,
    "Event" AS event,
    "Type" AS type,
    "Date" AS date,
    "Link" AS link,
    "Snippet" AS snippet
FROM "fivethirtyeight-potential-candidates-2015-01-30-events"
