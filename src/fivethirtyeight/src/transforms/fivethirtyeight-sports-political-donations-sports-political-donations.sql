-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Owner" AS owner,
    "Team" AS team,
    "League" AS league,
    "Recipient" AS recipient,
    "Amount" AS amount,
    "Election Year" AS election_year,
    "Party" AS party
FROM "fivethirtyeight-sports-political-donations-sports-political-donations"
