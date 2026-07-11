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
    "LAMBERT_93_X" AS lambert_93_x,
    "LAMBERT_93_Y" AS lambert_93_y,
    "ADRESSE" AS adresse,
    "NOM_COMMUNE" AS nom_commune,
    "CODE_GRAND_SECTEUR" AS code_grand_secteur,
    "CONSO" AS conso,
    "PDL" AS pdl
FROM "sdes-d46ca79f-6d07-4fb0-bac7-efc9b48e4239"
