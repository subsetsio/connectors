-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "route__id" AS route_id,
    "route_name",
    "sector",
    "property_number",
    "property_sequence",
    "route_updated_date",
    "property_updated_date",
    "route_active",
    "property_active"
FROM "nyc-open-data-752y-qk8b"
