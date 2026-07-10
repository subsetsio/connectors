-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "date",
    "champ",
    "nomenclature",
    "code_naf",
    "libelle_naf",
    "type_de_donnees",
    "nombre_d_emplois_vacants",
    "taux_d_emplois_vacants_en"
FROM "dares-dares-emploivacants-brut-emploisvacants"
