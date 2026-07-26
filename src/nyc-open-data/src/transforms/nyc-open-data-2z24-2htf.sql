-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "intake_date",
    "_source" AS source,
    "_language" AS language,
    "request_type",
    "topic",
    "outcome",
    "industry",
    "city",
    "state",
    "zip",
    "borough_name",
    "community_district",
    "council_district"
FROM "nyc-open-data-2z24-2htf"
