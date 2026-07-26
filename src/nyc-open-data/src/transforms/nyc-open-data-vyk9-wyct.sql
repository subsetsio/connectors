-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_year" AS year,
    "development",
    "borough",
    "city_council_district",
    "number_of_public_housing_residents_who_took_a_city_civil_service_exam"
FROM "nyc-open-data-vyk9-wyct"
