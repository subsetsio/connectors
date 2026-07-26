-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "treatment",
    "date",
    "nodeid",
    "wkt_geometry",
    "x",
    "y"
FROM "nyc-open-data-uh2s-ftgh"
