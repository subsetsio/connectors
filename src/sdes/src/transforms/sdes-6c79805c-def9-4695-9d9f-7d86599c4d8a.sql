-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "DEPARTEMENT_CODE" AS departement_code,
    "DEPARTEMENT_LIBELLE" AS departement_libelle,
    "REGION_CODE" AS region_code,
    "REGION_LIBELLE" AS region_libelle,
    "ANNEE" AS annee,
    "ESSENCE_M3" AS essence_m3,
    "GAZOLE_M3" AS gazole_m3,
    "FIOUL_M3" AS fioul_m3,
    "GPL_M3" AS gpl_m3,
    "CARBUREACTEUR_M3" AS carbureacteur_m3
FROM "sdes-6c79805c-def9-4695-9d9f-7d86599c4d8a"
