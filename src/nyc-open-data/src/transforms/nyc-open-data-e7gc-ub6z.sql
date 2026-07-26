-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "objectid",
    "cornerid",
    "street_name1",
    "street_name2",
    "borough",
    "construction_type",
    "construction_end_date",
    "construction_status_value"
FROM "nyc-open-data-e7gc-ub6z"
