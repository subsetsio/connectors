-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "OPERATEUR" AS operateur,
    "ANNEE" AS annee,
    "FILIERE" AS filiere,
    "CODE_EPCI_CODE" AS code_epci_code,
    "CODE_EPCI_LIBELLE" AS code_epci_libelle,
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
    "CODE_EIC" AS code_eic
FROM "sdes-d676a3a5-4eca-417d-bebc-754de9c1ca1c"
