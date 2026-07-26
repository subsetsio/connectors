-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "school_year",
    "report_type",
    "demographic_category",
    "dbn",
    "location_name",
    "location_category",
    "administrative_district",
    "student_count"
FROM "nyc-open-data-2t89-756w"
