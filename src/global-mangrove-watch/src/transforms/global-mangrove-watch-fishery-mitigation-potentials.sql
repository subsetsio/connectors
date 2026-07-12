-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "location_id",
    "iso",
    "location_type",
    "location_name",
    "indicator",
    "indicator_type",
    "value"
FROM "global-mangrove-watch-fishery-mitigation-potentials"
