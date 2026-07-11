-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "OPERATEUR" AS operateur,
    "ANNEE" AS annee,
    "FILIERE" AS filiere,
    "CODE_IRIS_CODE" AS code_iris_code,
    "CODE_IRIS_LIBELLE" AS code_iris_libelle,
    "CODE_CATEGORIE_CONSOMMATION" AS code_categorie_consommation,
    "CODE_SECTEUR_NAF2_CODE" AS code_secteur_naf2_code,
    "CODE_SECTEUR_NAF2_LIBELLE" AS code_secteur_naf2_libelle,
    "CODE_GRAND_SECTEUR" AS code_grand_secteur,
    "CONSO" AS conso,
    "PDL" AS pdl,
    "INDQUAL" AS indqual,
    "THERMOR" AS thermor,
    "PART" AS part,
    "CODE_EIC" AS code_eic,
    "NOM_COMMUNE" AS nom_commune,
    "CODE_IRIS_CORR" AS code_iris_corr
FROM "sdes-f88a1c55-0f24-4dac-9ac5-e151caf745e8"
