-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("annee" AS BIGINT) AS annee,
    "inscrits_en_1ere_annee",
    "inscrits_en_1ere_annee_hors_kinesitherapeutes",
    "diplomes",
    "diplomes_hors_kinesitherapeutes"
FROM "drees-graphique-ecole-sante"
