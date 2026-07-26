-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "unitid",
    "latitude",
    "longitude",
    "point_x",
    "point_y"
FROM "nyc-open-data-2w2g-fk3i"
