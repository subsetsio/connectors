-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "nationality",
    "gender",
    "affected_person_location",
    "result_of_the_accident",
    "number_of_people",
    "result_of_the_accident_ar",
    "affected_person_location_ar",
    "gender_ar",
    "nationality_ar"
FROM "qatar-planning-and-statistics-authority-number-of-deaths-and-injuries-from-traffic-accidents-by-nationality-gender-and-affected-person-location"
