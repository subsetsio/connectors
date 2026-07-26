-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "schoolyear",
    "dbn",
    "location_name",
    "location_type",
    "total_sw_gc",
    "total_gc",
    "full_time",
    "part_time",
    "bilingual",
    "serving_more_than_one_location",
    "atr",
    "sy201415_enrollment",
    "ratio_gc_sw",
    "ratio_gc_only"
FROM "nyc-open-data-wssh-seqa"
