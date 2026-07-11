-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "OPERATEUR" AS operateur,
    "CODE_EIC" AS code_eic,
    "ANNEE" AS annee,
    "FILIERE" AS filiere,
    "CODE_CATEGORIE_CONSOMMATION" AS code_categorie_consommation,
    "CODE_SECTEUR_NAF2_CODE" AS code_secteur_naf2_code,
    "CODE_SECTEUR_NAF2_LIBELLE" AS code_secteur_naf2_libelle,
    "CODE_GRAND_SECTEUR" AS code_grand_secteur,
    "CONSO" AS conso,
    "PDL" AS pdl,
    "INDQUAL" AS indqual,
    "THERMOR" AS thermor,
    "PART" AS part,
    "NB_IRIS_MASQUES" AS nb_iris_masques,
    "CODE_REGION_CODE" AS code_region_code,
    "CODE_REGION_LIBELLE" AS code_region_libelle
FROM "sdes-e841c15d-03e0-4289-b336-8c97b2d3a594"
