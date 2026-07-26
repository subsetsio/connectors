-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "service_at_location_id",
    "service_id",
    "location_id",
    "phone",
    "url",
    "budget"
FROM "nyc-open-data-8gr8-ngjc"
