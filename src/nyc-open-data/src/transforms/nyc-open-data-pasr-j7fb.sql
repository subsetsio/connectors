-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "incident_type",
    "_location" AS location,
    "borough",
    "creation_date",
    "closed_date",
    "latitude",
    "longitude"
FROM "nyc-open-data-pasr-j7fb"
