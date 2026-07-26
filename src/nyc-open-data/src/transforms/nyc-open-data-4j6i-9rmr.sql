-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ulurp_application_name",
    "community_boards",
    "council_districts",
    "ulurp_numbers",
    "borough_president_recommendation",
    "recommendation_date"
FROM "nyc-open-data-4j6i-9rmr"
