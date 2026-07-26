-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "tlid",
    "fnode",
    "tnode",
    "length",
    "fedirp",
    "fename",
    "fetype",
    "fedirs",
    "cfcc",
    "fraddl",
    "toaddl",
    "fraddr",
    "toaddr",
    "zipl",
    "zipr",
    "census1",
    "census2",
    "cfcc1",
    "cfcc2",
    "_source" AS source,
    "shape_leng"
FROM "nyc-open-data-kun8-kdsr"
