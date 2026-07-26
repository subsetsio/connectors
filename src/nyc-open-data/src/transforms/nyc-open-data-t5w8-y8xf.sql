-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "borough",
    "geo_district_ofbuildings",
    "building_ids",
    "dbn",
    "school_name"
FROM "nyc-open-data-t5w8-y8xf"
