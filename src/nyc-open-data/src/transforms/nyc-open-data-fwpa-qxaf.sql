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
    "street",
    "segmentid",
    "rank",
    "pmp_id",
    "nta2020",
    "boro",
    "category",
    "ntaname",
    "femafldz",
    "femafldt",
    "hrcevac",
    "shape_leng"
FROM "nyc-open-data-fwpa-qxaf"
