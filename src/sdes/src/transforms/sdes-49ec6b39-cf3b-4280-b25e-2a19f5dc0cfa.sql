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
    "PDL" AS pdl,
    "BAN_ADRESSE" AS ban_adresse,
    "BAN_QUALITE" AS ban_qualite,
    "BAN_NIVEAU" AS ban_niveau,
    "BAN_ID" AS ban_id
FROM "sdes-49ec6b39-cf3b-4280-b25e-2a19f5dc0cfa"
