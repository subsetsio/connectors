-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "type_of_service_ar",
    "type_of_service",
    "number_of_operations",
    "deaths",
    "serious_injuries",
    "simple_injuries"
FROM "qatar-planning-and-statistics-authority-rescue-and-relief-services-furnished-by-civil-defense-department-by-number-of-operations-injuries-deaths-and-type-of-service"
