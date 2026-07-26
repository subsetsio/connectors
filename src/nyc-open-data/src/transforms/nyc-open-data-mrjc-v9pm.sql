-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "geoid",
    "fshri",
    "fvi_storm_surge_present",
    "fvi_storm_surge_2050s",
    "fvi_storm_surge_2080s",
    "fvi_tidal_2020s",
    "fvi_tidal_2050s",
    "fvi_tidal_2080s"
FROM "nyc-open-data-mrjc-v9pm"
