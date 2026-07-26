-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "objectid_1",
    "street",
    "streetcode",
    "routetype",
    "boroname",
    "restrictio",
    "borocode",
    "truckroute",
    "ltdlocal",
    "nyc_reg",
    "segmentid",
    "shape_leng",
    "localtunl",
    "localbrg",
    "thrutunl",
    "thrubrg",
    "assem_dist",
    "cong_dist",
    "coun_dist",
    "st_sen_dis",
    "thruexwy",
    "borocd"
FROM "nyc-open-data-jjja-shxy"
