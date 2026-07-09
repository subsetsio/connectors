-- Published pass-through of raw asset `cnam-depenses`.
-- `tri` (portal sort order) is dropped. National totals only — this export carries no territory dimension.
SELECT
    CAST(EXTRACT(YEAR FROM "annee") AS BIGINT) AS year,
    "patho_niv1" AS pathology_level_1,
    "patho_niv2" AS pathology_level_2,
    "patho_niv3" AS pathology_level_3,
    "top" AS pathology_code,
    "dep_niv_1" AS spending_category,
    "dep_niv_2" AS spending_post,
    "type_somme" AS amount_type,
    "montant" AS amount_eur,
    "montant_moy" AS mean_amount_eur,
    "ntop" AS patients_with_pathology,
    "n_recourant_au_poste" AS patients_using_post,
    "niveau_prioritaire" AS priority_levels
FROM "cnam-depenses"
