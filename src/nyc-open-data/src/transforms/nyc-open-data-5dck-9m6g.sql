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
    "plazaname",
    "boro",
    "onstreet",
    "fromstreet",
    "tostreet",
    "partner",
    "femafldz",
    "femafldt",
    "hrcevac",
    "point_x",
    "point_y"
FROM "nyc-open-data-5dck-9m6g"
