-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_year" AS year,
    "city_council_district",
    "borough",
    "number_of_public_housing_residents_enrolled_in_courses_or_otherwise_received_guidance"
FROM "nyc-open-data-8zxg-9a5c"
