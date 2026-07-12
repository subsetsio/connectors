-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "dispositif",
    "code_region",
    "region",
    "code_ancienne_region",
    "ancienne_region",
    "code_departement",
    "departement",
    "code_na21",
    "secteur_na21",
    "nombre_de_beneficiaires",
    "montant_total_de_l_aide",
    "montant_en_millions",
    "geo_point_2d"
FROM "urssaf-aide-exceptionnelle-cpsti-covid-19"
