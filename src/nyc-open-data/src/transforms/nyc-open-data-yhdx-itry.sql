-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "vms",
    "main_roadway",
    "direction",
    "cross_street",
    "borough",
    "borocode",
    "borocd",
    "coundist",
    "assemdist",
    "stsendist",
    "congdist",
    "_type" AS type,
    "_owner" AS owner,
    "femafldz",
    "femafldt",
    "hrcevac",
    "latitude",
    "longitude",
    "the_geom"
FROM "nyc-open-data-yhdx-itry"
