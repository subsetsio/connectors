-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "dbn",
    "_location" AS location,
    "location_type",
    "total_sw_gc",
    "total_sw",
    "full_time",
    "part_time",
    "bilingual",
    "serving_more_than_one_location",
    "atr"
FROM "nyc-open-data-vxxs-iyt2"
