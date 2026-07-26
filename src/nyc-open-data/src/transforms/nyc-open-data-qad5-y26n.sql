-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "id",
    "xmin",
    "xmax",
    "ymin",
    "ymax"
FROM "nyc-open-data-qad5-y26n"
