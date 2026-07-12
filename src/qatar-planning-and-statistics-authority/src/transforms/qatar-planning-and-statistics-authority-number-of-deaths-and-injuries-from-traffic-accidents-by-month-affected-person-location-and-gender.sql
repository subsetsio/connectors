-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "month",
    "lshhr",
    "affected_person_location",
    "result_of_the_accident_ar",
    "gender",
    "gender_ar",
    "result_of_the_accident",
    "affected_person_location_ar",
    "number_of_people"
FROM "qatar-planning-and-statistics-authority-number-of-deaths-and-injuries-from-traffic-accidents-by-month-affected-person-location-and-gender"
