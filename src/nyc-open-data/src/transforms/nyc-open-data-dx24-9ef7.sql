-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "boro",
    "block",
    "lot",
    "bbl",
    "_type" AS type,
    "shape_star",
    "shape_stle"
FROM "nyc-open-data-dx24-9ef7"
