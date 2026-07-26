-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "boro",
    "unitid",
    "point_x",
    "point_y",
    "cb",
    "latitude",
    "longitude"
FROM "nyc-open-data-5bgh-vtsn"
