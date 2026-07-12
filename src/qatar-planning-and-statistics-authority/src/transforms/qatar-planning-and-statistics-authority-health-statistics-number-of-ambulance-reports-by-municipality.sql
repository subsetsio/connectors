-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "al_daayen",
    "al_khor_lkhwr",
    "al_rayyan",
    "al_shamal",
    "al_wakrah",
    "doha",
    "umm_salal",
    "unknown"
FROM "qatar-planning-and-statistics-authority-health-statistics-number-of-ambulance-reports-by-municipality"
