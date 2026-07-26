-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "modzcta",
    "_label" AS label,
    "zcta",
    "pop_est",
    "the_geom"
FROM "nyc-open-data-pri4-ifjk"
