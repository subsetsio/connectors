-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "OPERATEUR" AS operateur,
    "ANNEE" AS annee,
    "FILIERE" AS filiere,
    "IRIS_CODE" AS iris_code,
    "IRIS_LIBELLE" AS iris_libelle,
    "CODE_GRAND_SECTEUR" AS code_grand_secteur,
    "CONSO" AS conso,
    "PDL" AS pdl
FROM "sdes-9aae15ac-70be-4c07-bd6d-069a12bc481f"
