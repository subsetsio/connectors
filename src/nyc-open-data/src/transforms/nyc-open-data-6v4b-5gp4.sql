-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "unit",
    "group_namepartner",
    "date_and_time",
    "borough",
    "locationtype",
    "_location" AS location,
    "event_name",
    "event_type",
    "category",
    "classification",
    "attendance",
    "audience",
    "_source" AS source
FROM "nyc-open-data-6v4b-5gp4"
