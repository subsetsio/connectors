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
    "LAMBERT_93_X" AS lambert_93_x,
    "LAMBERT_93_Y" AS lambert_93_y,
    "ADRESSE" AS adresse,
    "NOM_COMMUNE" AS nom_commune,
    "CODE_GRAND_SECTEUR" AS code_grand_secteur,
    "CONSO" AS conso,
    "PDL" AS pdl
FROM "sdes-6c26ab2e-29e0-46ab-b8d6-737dc3f2a2e2"
