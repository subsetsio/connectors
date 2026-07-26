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
    "_location" AS location,
    "borough",
    "date_insta",
    "point_x",
    "point_y",
    "femafldz",
    "femafldt",
    "hrcevac",
    "ntaname"
FROM "nyc-open-data-de3m-c5p4"
