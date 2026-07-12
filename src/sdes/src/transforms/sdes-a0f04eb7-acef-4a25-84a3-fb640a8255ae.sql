-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("OPERATEUR" AS VARCHAR) AS operateur,
    CAST("ANNEE" AS BIGINT) AS annee,
    CAST("FILIERE" AS VARCHAR) AS filiere,
    CAST("CODE_IRIS_CODE" AS VARCHAR) AS code_iris_code,
    CAST("CODE_IRIS_LIBELLE" AS VARCHAR) AS code_iris_libelle,
    CAST("CODE_GRAND_SECTEUR" AS VARCHAR) AS code_grand_secteur,
    CAST("CONSO" AS DOUBLE) AS conso,
    CAST("PDL" AS BIGINT) AS pdl,
    CAST("NOM_COMMUNE" AS VARCHAR) AS nom_commune,
    CAST("ADRESSE" AS VARCHAR) AS adresse,
    CAST("CODE_EIC" AS VARCHAR) AS code_eic,
    CAST("CODE_SECTEUR_NAF2_CODE" AS VARCHAR) AS code_secteur_naf2_code,
    CAST("CODE_SECTEUR_NAF2_LIBELLE" AS VARCHAR) AS code_secteur_naf2_libelle,
    CAST("ALERTE_CONSO_IRIS" AS BOOLEAN) AS alerte_conso_iris,
    CAST("CODE_IRIS_CORR" AS VARCHAR) AS code_iris_corr,
    CAST("BAN_LATITUDE" AS DOUBLE) AS ban_latitude,
    CAST("BAN_LONGITUDE" AS DOUBLE) AS ban_longitude,
    CAST("BAN_ADRESSE" AS VARCHAR) AS ban_adresse,
    CAST("BAN_QUALITE" AS DOUBLE) AS ban_qualite,
    CAST("BAN_NIVEAU" AS VARCHAR) AS ban_niveau,
    CAST("BAN_ID" AS VARCHAR) AS ban_id
FROM "sdes-a0f04eb7-acef-4a25-84a3-fb640a8255ae"
