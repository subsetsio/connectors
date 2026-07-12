-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "mois_d_echeance",
    "categorie_de_ti",
    "grand_secteur_d_activite",
    "secteur_na38",
    "secteur_na88",
    "nombre_de_ti_concernes",
    "montant_des_reports",
    "montant_en_millions"
FROM "urssaf-mesures-exceptionnelles-covid-19-reports-ti-france-entiere"
