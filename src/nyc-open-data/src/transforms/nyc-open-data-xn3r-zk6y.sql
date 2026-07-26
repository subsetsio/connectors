-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "borocode",
    "boroname",
    "countyfips",
    "cdta2020",
    "cdtaname",
    "cdtatype",
    "shape_length",
    "shape_area",
    "the_geom"
FROM "nyc-open-data-xn3r-zk6y"
