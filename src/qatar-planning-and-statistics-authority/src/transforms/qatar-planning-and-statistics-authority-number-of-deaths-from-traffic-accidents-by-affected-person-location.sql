-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "affected_person_location",
    "number_of_deaths",
    "affected_person_location_ar"
FROM "qatar-planning-and-statistics-authority-number-of-deaths-from-traffic-accidents-by-affected-person-location"
