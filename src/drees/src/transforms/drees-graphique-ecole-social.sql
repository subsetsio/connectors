-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("annee" AS BIGINT) AS annee,
    "effectifs_totaux_d_inscrits",
    "effectifs_d_inscrits_en_premiere_annee",
    "effectifs_de_diplomes"
FROM "drees-graphique-ecole-social"
