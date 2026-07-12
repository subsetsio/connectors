-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "annee",
    "type_de_travailleur_independant",
    "trimestre",
    "dernier_jour_du_trimestre",
    "nombre_de_ti_actifs"
FROM "urssaf-travailleurs-independants-actifs-trimestriels"
