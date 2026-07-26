-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "ctlabel",
    "borocode",
    "boroname",
    "ct2020",
    "boroct2020",
    "cdeligibil",
    "ntaname",
    "nta2020",
    "cdta2020",
    "cdtaname",
    "geoid",
    "shape_length",
    "shape_area"
FROM "nyc-open-data-63ge-mke6"
