-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "borocode",
    "boroname",
    "countyfips",
    "nta2020",
    "ntaname",
    "ntaabbrev",
    "ntatype",
    "cdta2020",
    "cdtaname",
    "shape_length",
    "shape_area",
    "the_geom"
FROM "nyc-open-data-9nt8-h7nd"
