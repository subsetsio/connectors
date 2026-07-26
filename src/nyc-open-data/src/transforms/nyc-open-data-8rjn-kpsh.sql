-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "treatment_" AS treatment,
    "unitid",
    "ownership",
    "_location" AS location,
    "latitude",
    "longitude",
    "point_x",
    "point_y",
    "outfall_ty",
    "of_size",
    "receiving_" AS receiving
FROM "nyc-open-data-8rjn-kpsh"
