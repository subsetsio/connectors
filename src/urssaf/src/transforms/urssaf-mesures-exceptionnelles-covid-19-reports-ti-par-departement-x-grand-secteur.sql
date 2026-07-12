-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "mois_d_echeance",
    "categorie_de_ti",
    "code_region",
    "region",
    "code_ancienne_region",
    "ancienne_region",
    "code_departement",
    "departement",
    "grand_secteur",
    "nombre_de_ti_concernes",
    "montant_des_reports",
    "montant_en_millions",
    "geo_point_2d"
FROM "urssaf-mesures-exceptionnelles-covid-19-reports-ti-par-departement-x-grand-secteur"
