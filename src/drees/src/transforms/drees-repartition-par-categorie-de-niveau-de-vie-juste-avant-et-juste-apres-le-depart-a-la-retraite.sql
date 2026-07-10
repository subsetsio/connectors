-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("premiere_annee_pleine_de_retraite" AS BIGINT) AS premiere_annee_pleine_de_retraite,
    "caracteristique",
    "categorie",
    "annee_d_observation_du_groupe_de_niveau_de_vie",
    "sexe",
    "groupe_de_niveau_de_vie",
    "part_du_groupe_de_niveau_de_vie_au_sein_de_la_categorie",
    "part_de_la_categorie_au_sein_du_groupe_de_niveau_de_vie"
FROM "drees-repartition-par-categorie-de-niveau-de-vie-juste-avant-et-juste-apres-le-depart-a-la-retraite"
