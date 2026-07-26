-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "cb2010",
    "borocode",
    "boroname",
    "ct2010",
    "bctcb2010",
    "shape_area",
    "shape_length",
    "the_geom"
FROM "nyc-open-data-y9w2-ph8n"
