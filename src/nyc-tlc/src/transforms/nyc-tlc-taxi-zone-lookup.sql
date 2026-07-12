-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "LocationID" AS locationid,
    "Borough" AS borough,
    "Zone" AS zone,
    "service_zone"
FROM "nyc-tlc-taxi-zone-lookup"
