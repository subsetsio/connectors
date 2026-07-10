-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("premiere_annee_pleine_de_retraite" AS BIGINT) AS premiere_annee_pleine_de_retraite,
    "caracteristique",
    "categorie",
    "sexe",
    "revenu_utilise_pour_le_calcul_du_taux_de_remplacement",
    "taux_de_remplacement_quantile_a_10",
    "taux_de_remplacement_quantile_a_25",
    "taux_de_remplacement_quantile_a_50",
    "taux_de_remplacement_quantile_a_75",
    "taux_de_remplacement_quantile_a_90",
    "part_de_la_categorie_ayant_un_taux_de_remplacement_inferieur_a_100_en"
FROM "drees-repartition-des-taux-de-remplacement-entre-les-revenus-juste-avant-et-juste-apres-la-retraite"
