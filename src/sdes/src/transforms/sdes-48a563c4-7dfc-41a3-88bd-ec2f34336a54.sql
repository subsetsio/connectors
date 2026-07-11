-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "OPERATEUR" AS operateur,
    "CODE_EIC" AS code_eic,
    "ANNEE" AS annee,
    "FILIERE" AS filiere,
    "CODE_IRIS_CODE" AS code_iris_code,
    "CODE_IRIS_LIBELLE" AS code_iris_libelle,
    "CODE_GRAND_SECTEUR" AS code_grand_secteur,
    "CONSO" AS conso,
    "PDL" AS pdl,
    "NOM_COMMUNE" AS nom_commune,
    "ADRESSE" AS adresse,
    "CODE_SECTEUR_NAF2_CODE" AS code_secteur_naf2_code,
    "CODE_SECTEUR_NAF2_LIBELLE" AS code_secteur_naf2_libelle,
    "ALERTE_CONSO_IRIS" AS alerte_conso_iris,
    "BAN_LATITUDE" AS ban_latitude,
    "BAN_LONGITUDE" AS ban_longitude,
    "BAN_ADRESSE" AS ban_adresse,
    "BAN_QUALITE" AS ban_qualite,
    "BAN_NIVEAU" AS ban_niveau,
    "BAN_ID" AS ban_id
FROM "sdes-48a563c4-7dfc-41a3-88bd-ec2f34336a54"
