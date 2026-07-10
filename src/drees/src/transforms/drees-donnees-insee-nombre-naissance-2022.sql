-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "code_departement",
    "nom_departement",
    "taux_de_natalite_en_2023_en_0",
    "age_moyen_de_la_mere_a_la_naissance_en_2023",
    "nombre_de_naissances_vivantes_domiciliees_en_2022"
FROM "drees-donnees-insee-nombre-naissance-2022"
