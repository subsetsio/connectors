-- Published pass-through of raw asset `cnam-honoraires-detailles`.
-- the `vision_*` portal display flags are dropped.
SELECT
    CAST(EXTRACT(YEAR FROM "annee") AS BIGINT) AS year,
    "profession_sante" AS profession,
    "region" AS region_code,
    "libelle_region" AS region_name,
    "departement" AS department_code,
    "libelle_departement" AS department_name,
    "honoraires_ordre_niv_1" AS fee_level_1_code,
    "type_honoraires_niveau_1" AS fee_level_1,
    "honoraires_ordre_niv_2" AS fee_level_2_code,
    "type_honoraires_niveau_2" AS fee_level_2,
    "honoraires_ordre_niv_3" AS fee_level_3_code,
    "type_honoraires_niveau_3" AS fee_level_3,
    "montant_honoraires" AS fees_eur,
    "montant_honoraires_moyens" AS mean_fees_eur
FROM "cnam-honoraires-detailles"
