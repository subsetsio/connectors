-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "geo_level",
    "geo_unit",
    "voted",
    "did_not_vote",
    "not_eligible_to_vote",
    "turnout",
    "election",
    "election_date",
    "_year" AS year
FROM "nyc-open-data-rixx-fc37"
