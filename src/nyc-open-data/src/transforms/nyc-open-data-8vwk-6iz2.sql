-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_year" AS year,
    "market_name",
    "borough",
    "street_address",
    "community_district",
    "latitude",
    "longitude",
    "days_of_operation",
    "hours_of_operations",
    "season_dates",
    "accepts_ebt",
    "open_yearround",
    "stellar_cooking_demonstrations"
FROM "nyc-open-data-8vwk-6iz2"
