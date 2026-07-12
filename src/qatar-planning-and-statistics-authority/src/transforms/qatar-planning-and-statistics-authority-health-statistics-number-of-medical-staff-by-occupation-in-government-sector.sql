-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year_lsn",
    "allied_health_professional_ml_fy_lmhn_lshy_lms_d",
    "dentist_tbyb_snn",
    "nurse_mmrd_w_mmrd",
    "pharmacist_sydly",
    "physician_tbyb"
FROM "qatar-planning-and-statistics-authority-health-statistics-number-of-medical-staff-by-occupation-in-government-sector"
