-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "system_code",
    "location_name",
    "location_category_description",
    "administrative_district_code",
    "grade_04",
    "grade_05",
    "grade_06",
    "grade_07",
    "grade_08",
    "grade_09",
    "grade_10",
    "grade_11",
    "grade_12",
    "total_removalssuspensions_where_nypd_was_contacted"
FROM "nyc-open-data-2eq2-nywg"
