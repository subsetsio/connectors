-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_name" AS name,
    "unique_id",
    "_type" AS type,
    "street_address",
    "boroughcity",
    "state",
    "zipcode",
    "latitude",
    "longitude",
    "point"
FROM "nyc-open-data-ufxk-pq9j"
