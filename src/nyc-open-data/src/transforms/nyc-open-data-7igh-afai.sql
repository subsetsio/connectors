-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "boroname",
    "ctlabel",
    "the_geom",
    "borocode",
    "ct2000",
    "boroct2000",
    "cdeligibil",
    "ntacode",
    "ntaname",
    "puma",
    "shape_leng",
    "shape_area"
FROM "nyc-open-data-7igh-afai"
