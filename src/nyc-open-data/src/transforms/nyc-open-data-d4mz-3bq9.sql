-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "school_year",
    "dbn",
    "_location" AS location,
    "location_type",
    "total_sw",
    "fulltime",
    "parttime",
    "bilingual",
    "serving_more_than_one_location",
    "unnamed_column"
FROM "nyc-open-data-d4mz-3bq9"
