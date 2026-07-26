-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "borocode",
    "boroname",
    "borocd",
    "coundist",
    "assemdist",
    "stsendist",
    "congdist",
    "siteid",
    "benchid",
    "category",
    "benchtype",
    "installati",
    "address",
    "geocodeadd",
    "street",
    "crossstree",
    "borough",
    "comdist",
    "busroute",
    "bid",
    "latitude",
    "longitude",
    "femafldz",
    "femafldt",
    "hrcevac"
FROM "nyc-open-data-kuxa-tauh"
