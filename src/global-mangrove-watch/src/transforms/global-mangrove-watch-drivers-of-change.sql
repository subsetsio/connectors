-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "location_id",
    "iso",
    "location_type",
    "location_name",
    "variable",
    "primary_driver",
    "value"
FROM "global-mangrove-watch-drivers-of-change"
