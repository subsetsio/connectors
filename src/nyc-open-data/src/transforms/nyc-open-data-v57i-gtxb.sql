-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "borobox",
    "box_type",
    "_location" AS location,
    "zip",
    "borough",
    "communitydistict",
    "citycouncil",
    "latitude",
    "longitude",
    "location_point"
FROM "nyc-open-data-v57i-gtxb"
