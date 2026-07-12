-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "systeme_declaratif",
    "region",
    "ancienne_region",
    "nom_du_departement",
    "code_region",
    "code_ancienne_region",
    "code_departement",
    "nombre_d_employeurs",
    "nombre_de_salaries",
    "nombre_d_heures",
    "salaire",
    "indemnisation_versee_estimee",
    "montant_rembourse"
FROM "urssaf-mesures-exceptionnelles-covid-19-indemnisation-activite-partielle-emploi-domicil"
