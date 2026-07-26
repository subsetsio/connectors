-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "ctlabel",
    "borocode",
    "boroname",
    "ct2010",
    "boroct2010",
    "cdeligibil",
    "ntacode",
    "ntaname",
    "puma",
    "shape_area",
    "shape_length"
FROM "nyc-open-data-ht7m-2uh6"
