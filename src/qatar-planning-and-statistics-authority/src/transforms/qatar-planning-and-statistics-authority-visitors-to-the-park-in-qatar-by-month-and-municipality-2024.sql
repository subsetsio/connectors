-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "months",
    "months_ar",
    "doha",
    "al_rayyan",
    "umm_salal",
    "al_shahanniya",
    "al_wakarah",
    "al_khor_zakira",
    "al_daayen",
    "al_shamal"
FROM "qatar-planning-and-statistics-authority-visitors-to-the-park-in-qatar-by-month-and-municipality-2024"
