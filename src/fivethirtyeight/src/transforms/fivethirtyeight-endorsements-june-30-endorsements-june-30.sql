-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "party",
    "candidate",
    "endorsement_points",
    "percentage_endorsement_points",
    "money_raised",
    "percentage_of_money",
    "primary_vote_percentage",
    "won_primary"
FROM "fivethirtyeight-endorsements-june-30-endorsements-june-30"
