-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "published_date",
    "neighborhood_tabulation_area",
    "health_events",
    "number_of_avoided_health_events_per_nta_resident"
FROM "nyc-open-data-ic46-fvh8"
