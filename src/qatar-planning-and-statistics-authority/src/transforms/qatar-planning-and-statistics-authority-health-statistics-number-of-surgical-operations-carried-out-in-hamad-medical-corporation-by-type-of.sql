-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "cardiac_surgery",
    "dental_surgery",
    "general_surgery",
    "gynecological_surgery",
    "neurosurgery_surgery",
    "obstetric_surgery",
    "ophthalmology_surgery",
    "orthopaedic_surgery",
    "otolaryngology_surgery",
    "paediatric_surgery",
    "plastic_surgery",
    "urological_surgery",
    "other"
FROM "qatar-planning-and-statistics-authority-health-statistics-number-of-surgical-operations-carried-out-in-hamad-medical-corporation-by-type-of"
