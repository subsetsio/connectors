-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("metric_month", '%Y-%m')::DATE AS metric_month,
    "industry",
    "pickupdropoff",
    "location_id",
    "borough",
    "_zone" AS zone,
    "trip_count"
FROM "nyc-open-data-c5iv-bn4s"
