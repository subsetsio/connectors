-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ID" AS id,
    "OPERATEUR" AS operateur,
    "ANNEE" AS annee,
    "IRIS_CODE" AS iris_code,
    "IRIS_LIBELLE" AS iris_libelle,
    "FILIERE" AS filiere,
    "CODE_GRAND_SECTEUR" AS code_grand_secteur,
    "CONSO" AS conso,
    "PDL" AS pdl
FROM "sdes-27ac7bef-c767-47bd-8657-fe3a4a035e9d"
