-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "borough",
    "boro_code",
    "route_name",
    "route_type",
    "route_sub",
    "route_stat"
FROM "nyc-open-data-eshd-3mzu"
