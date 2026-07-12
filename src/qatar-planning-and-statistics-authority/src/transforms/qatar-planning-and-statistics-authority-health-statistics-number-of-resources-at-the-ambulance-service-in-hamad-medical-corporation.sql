-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "number_of_helicopters",
    "number_of_rapid_response_units",
    "number_of_ambulances",
    "number_of_critical_care_paramedics",
    "number_of_ambulance_paramedics"
FROM "qatar-planning-and-statistics-authority-health-statistics-number-of-resources-at-the-ambulance-service-in-hamad-medical-corporation"
