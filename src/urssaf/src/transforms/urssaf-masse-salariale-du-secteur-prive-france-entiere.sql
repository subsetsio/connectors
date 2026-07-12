-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "annee",
    "trimestre",
    "dernier_jour_trim",
    "ms_t_50j_brut",
    "ms_t_60j_brut",
    "ms_t_50j_cvs",
    "ms_t_60j_cvs",
    "gt_ms_t_50j_cvs",
    "gt_ms_t_60j_cvs",
    "ga_ms_t_50j_cvs",
    "ga_ms_t_60j_cvs"
FROM "urssaf-masse-salariale-du-secteur-prive-france-entiere"
