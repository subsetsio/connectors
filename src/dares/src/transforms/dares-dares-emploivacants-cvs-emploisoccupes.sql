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
    "nombre_d_emplois_occupes"
FROM "dares-dares-emploivacants-cvs-emploisoccupes"
