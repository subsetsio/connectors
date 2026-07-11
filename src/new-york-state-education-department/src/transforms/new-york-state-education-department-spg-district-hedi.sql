-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Historical student-growth HEDI data covers the former evaluation regime and should not be treated as current educator evaluation coverage.
SELECT
    "report_year",
    "district_beds",
    "district_name",
    "district_needs",
    "per_pupil_expenditure",
    CAST("district_id" AS BIGINT) AS district_id,
    "hedi",
    "district_needs_category",
    "educator_id",
    "hedi_rating"
FROM "new-york-state-education-department-spg-district-hedi"
