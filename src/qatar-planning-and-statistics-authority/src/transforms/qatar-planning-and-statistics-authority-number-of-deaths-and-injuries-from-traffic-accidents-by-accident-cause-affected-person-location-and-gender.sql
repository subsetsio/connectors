-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "accident_cause",
    "affected_person_location",
    "gender",
    "result_of_the_accident",
    "number_of_people",
    "result_of_the_accident_ar",
    "gender_ar",
    "affected_person_location_ar",
    "cause_of_the_accident_ar"
FROM "qatar-planning-and-statistics-authority-number-of-deaths-and-injuries-from-traffic-accidents-by-accident-cause-affected-person-location-and-gender"
