-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "defnum",
    "initby",
    "housenum",
    "oft",
    "onfacename",
    "onprimname",
    "frmprimnam",
    "toprimname",
    "specloc",
    "boro",
    "_source" AS source,
    "rptdate",
    "rptclosed",
    "shape_leng"
FROM "nyc-open-data-x9wy-ing4"
