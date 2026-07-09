-- Published pass-through of raw asset `cnam-demographie-ages-moyens-part-des-femmes-part-des-plus-de-60-ans`.
-- the `vision_*` portal display flags are dropped (they live in `cnam-referentiel-professions`).
SELECT
    CAST(EXTRACT(YEAR FROM "annee") AS BIGINT) AS year,
    "profession_sante" AS profession,
    "part_femmes" AS share_women,
    "part_hommes" AS share_men,
    "part_des_60_ans_et_plus" AS share_aged_60_and_over,
    "part_des_moins_de_60_ans" AS share_aged_under_60,
    "age_moyen_global" AS mean_age,
    "age_moyen_femmes" AS mean_age_women,
    "age_moyen_hommes" AS mean_age_men
FROM "cnam-demographie-ages-moyens-part-des-femmes-part-des-plus-de-60-ans"
