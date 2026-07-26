-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "school_year",
    "report_category",
    "demographic_category",
    "dbn",
    "location_name",
    "location_category",
    "administrative_district",
    "students_with_2_or_more_suspensions_or_removals"
FROM "nyc-open-data-48wd-x25j"
