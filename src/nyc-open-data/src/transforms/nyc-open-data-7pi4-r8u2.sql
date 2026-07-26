-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "school_year",
    "dbn",
    "_location" AS location,
    "location_type",
    "total_gc_sw",
    "total_gc",
    "fulltime",
    "parttime",
    "bilingual",
    "serving_more_than_one_location",
    "atr",
    "_2014_enrollment_pk12" AS 2014_enrollment_pk12,
    "ratio_gc_sw",
    "ratio_gc_only",
    "unnamed_column",
    "unnamed_column_1",
    "unnamed_column_2",
    "unnamed_column_3"
FROM "nyc-open-data-7pi4-r8u2"
