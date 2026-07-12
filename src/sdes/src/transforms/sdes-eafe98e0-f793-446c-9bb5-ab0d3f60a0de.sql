-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("OPERATEUR" AS VARCHAR) AS operateur,
    CAST("ANNEE" AS BIGINT) AS annee,
    CAST("FILIERE" AS VARCHAR) AS filiere,
    CAST("CODE_EPCI_CODE" AS VARCHAR) AS code_epci_code,
    CAST("CODE_EPCI_LIBELLE" AS VARCHAR) AS code_epci_libelle,
    CAST("CODE_CATEGORIE_CONSOMMATION" AS VARCHAR) AS code_categorie_consommation,
    CAST("CODE_SECTEUR_NAF2_CODE" AS VARCHAR) AS code_secteur_naf2_code,
    CAST("CODE_SECTEUR_NAF2_LIBELLE" AS VARCHAR) AS code_secteur_naf2_libelle,
    CAST("CODE_GRAND_SECTEUR" AS VARCHAR) AS code_grand_secteur,
    CAST("CONSO" AS VARCHAR) AS conso,
    CAST("PDL" AS VARCHAR) AS pdl,
    CAST("INDQUAL" AS DOUBLE) AS indqual,
    CAST("THERMOR" AS BIGINT) AS thermor,
    CAST("PART" AS BIGINT) AS part,
    CAST("NB_IRIS_MASQUES" AS BIGINT) AS nb_iris_masques,
    CAST("CODE_EIC" AS VARCHAR) AS code_eic
FROM "sdes-eafe98e0-f793-446c-9bb5-ab0d3f60a0de"
