-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("annee" AS BIGINT) AS annee,
    "sans_reforme_mico_de_2023",
    "avec_reforme_mico_de_2023"
FROM "drees-graph-er-1297"
