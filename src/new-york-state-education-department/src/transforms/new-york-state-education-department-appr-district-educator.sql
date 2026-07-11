-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Historical APPR researcher data covers the former 2012-13 through 2015-16 evaluation regime and should not be treated as current educator evaluation coverage.
SELECT
    "report_year",
    "district_beds",
    "district_name",
    "district_needs",
    "per_pupil_expenditure",
    CAST("educator_id" AS BIGINT) AS educator_id,
    "overall_composite_score",
    "overall_composite_rating",
    "growth_rating",
    "local_rating",
    "other_rating",
    "district_needs_category",
    "overall_rating",
    "overall_score"
FROM "new-york-state-education-department-appr-district-educator"
