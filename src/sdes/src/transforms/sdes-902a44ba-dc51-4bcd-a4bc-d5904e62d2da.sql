-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ID" AS id,
    "OPERATEUR" AS operateur,
    "ANNEE" AS annee,
    "IRIS" AS iris,
    "IRIS_LIBELLE" AS iris_libelle,
    "FILIERE" AS filiere,
    "CODE_GRAND_SECTEUR" AS code_grand_secteur,
    "CONSO" AS conso,
    "PDL" AS pdl
FROM "sdes-902a44ba-dc51-4bcd-a4bc-d5904e62d2da"
