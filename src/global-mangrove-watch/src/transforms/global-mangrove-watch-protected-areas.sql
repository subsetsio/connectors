-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "location_id",
    "iso",
    "location_type",
    "location_name",
    "id",
    "year",
    "total_area",
    "protected_area"
FROM "global-mangrove-watch-protected-areas"
