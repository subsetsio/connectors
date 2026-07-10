-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("annees" AS BIGINT) AS annees,
    "autonomes_gir_5_ou_6",
    "besoin_d_aide_modere_gir_3_ou_4",
    "besoin_d_aide_important_gir_1_ou_2"
FROM "drees-graphique2b-er-livia"
