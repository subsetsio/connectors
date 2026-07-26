-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "objectid",
    "borocd",
    "assemdist",
    "coundist",
    "congdist",
    "stsendist",
    "plazaname",
    "onstreet",
    "fromstreet",
    "tostreet",
    "partner",
    "borocode",
    "boroname",
    "femafldz",
    "femafldt",
    "hrcevac",
    "shape_leng",
    "shape_area"
FROM "nyc-open-data-k5k6-6jex"
