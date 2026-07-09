-- Published pass-through of raw asset `cnam-comorbidites`.
-- `region` (99) and `dept` (999) are constant national codes in this export and are dropped.
SELECT
    CAST(EXTRACT(YEAR FROM "annee") AS BIGINT) AS year,
    "patho_niv1" AS pathology_level_1,
    "patho_niv2" AS pathology_level_2,
    "patho_niv3" AS pathology_level_3,
    "top" AS pathology_code,
    "comorbidite" AS comorbidity_code,
    "libelle_comorbidite" AS comorbidity,
    "patho_niv1_comorb" AS comorbidity_level_1,
    "patho_niv2_comorb" AS comorbidity_level_2,
    "patho_niv3_comorb" AS comorbidity_level_3,
    "ntop" AS patients_with_pathology,
    "ncomorb" AS patients_with_comorbidity,
    "proportion_comorb" AS comorbidity_share,
    "niveau_prioritaire" AS priority_levels
FROM "cnam-comorbidites"
