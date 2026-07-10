-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("annee" AS BIGINT) AS annee,
    "femmes",
    "hommes",
    "ensemble"
FROM "drees-retraite-graphique-1-age-conjoncturel-moyen-de-depart-a-la-retraite-selon-le-se0"
