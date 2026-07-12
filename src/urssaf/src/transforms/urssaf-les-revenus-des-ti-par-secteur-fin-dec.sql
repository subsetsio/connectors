-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "type_de_travailleur_independant",
    "secteur_d_activite",
    "annee",
    "nombre_de_ti",
    "revenu"
FROM "urssaf-les-revenus-des-ti-par-secteur-fin-dec"
