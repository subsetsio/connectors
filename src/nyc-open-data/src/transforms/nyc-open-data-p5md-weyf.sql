-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "city",
    "ec_name",
    "address",
    "zip_code",
    "borocode",
    "state",
    "accessible",
    "bin",
    "bbl"
FROM "nyc-open-data-p5md-weyf"
