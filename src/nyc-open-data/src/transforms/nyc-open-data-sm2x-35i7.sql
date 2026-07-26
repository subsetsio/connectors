-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "treatment_" AS treatment,
    "completion",
    "long",
    "lat",
    "x",
    "y"
FROM "nyc-open-data-sm2x-35i7"
