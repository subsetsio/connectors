-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "doha",
    "al_rayan",
    "al_wakra",
    "umm_salal",
    "al_khor_al_thakira",
    "al_shamal",
    "al_daayen",
    "al_shahaniya"
FROM "qatar-planning-and-statistics-authority-youth-and-sports-institutions-by-municipality"
