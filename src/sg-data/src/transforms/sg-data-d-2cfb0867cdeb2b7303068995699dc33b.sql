-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "VenueName" AS venuename,
    "PostalCode" AS postalcode,
    "Latitude" AS latitude,
    "Longitude" AS longitude,
    "SportsFacility" AS sportsfacility
FROM "sg-data-d-2cfb0867cdeb2b7303068995699dc33b"
