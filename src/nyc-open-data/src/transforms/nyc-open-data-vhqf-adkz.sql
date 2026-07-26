-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "greater_transit_zone_for_qualifying_sites",
    "shape_length",
    "shape_area"
FROM "nyc-open-data-vhqf-adkz"
