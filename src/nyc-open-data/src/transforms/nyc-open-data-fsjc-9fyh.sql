-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "parksid",
    "block",
    "lotnum",
    "lotsize",
    "areacovered"
FROM "nyc-open-data-fsjc-9fyh"
