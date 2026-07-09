-- Published pass-through of raw asset `cnam-referentiel-pathologies`.
-- `tri` (portal sort order) and `texte_d_avertissement` (constant `NA`) are dropped.
SELECT
    "patho_niv1" AS pathology_level_1,
    "patho_niv2" AS pathology_level_2,
    "patho_niv3" AS pathology_level_3,
    "top" AS pathology_code,
    "top_facet" AS pathology_facet_code,
    CAST("niveau_de_l_arborescence" AS BIGINT) AS hierarchy_level,
    "patho_niv1_comorb" AS comorbidity_level_1,
    "patho_niv2_comorb" AS comorbidity_level_2,
    "patho_niv3_comorb" AS comorbidity_level_3,
    "niveau_prioritaire" AS priority_levels
FROM "cnam-referentiel-pathologies"
