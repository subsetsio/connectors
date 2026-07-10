-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Person" AS person,
    "Party" AS party,
    "Statement Date" AS statement_date,
    "Latest Statement" AS latest_statement,
    "Statement Score" AS statement_score
FROM "fivethirtyeight-potential-candidates-2015-01-30-statements"
