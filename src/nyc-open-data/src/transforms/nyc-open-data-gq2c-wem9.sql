-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "date",
    "_event" AS event,
    "address",
    "long",
    "lat",
    "x",
    "y"
FROM "nyc-open-data-gq2c-wem9"
