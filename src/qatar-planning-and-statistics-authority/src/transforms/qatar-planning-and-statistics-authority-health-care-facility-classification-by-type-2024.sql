-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "health_care_facility_classification",
    "number"
FROM "qatar-planning-and-statistics-authority-health-care-facility-classification-by-type-2024"
