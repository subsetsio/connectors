-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "quartersec",
    "zoning_map",
    "section",
    "the_geom",
    "westmap",
    "eastmap",
    "northmap",
    "southmap",
    "northwestm",
    "northeastm",
    "southwestm",
    "southeastm",
    "shape_leng",
    "shape_area"
FROM "nyc-open-data-wwcv-s7e7"
