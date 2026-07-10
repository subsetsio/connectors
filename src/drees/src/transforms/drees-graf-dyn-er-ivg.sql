-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("annee" AS BIGINT) AS annee,
    "ivg_hors_etablissement_de_sante",
    "ivg_instrumentales_en_etablissement",
    "ivg_medicamenteuses_en_etablissement"
FROM "drees-graf-dyn-er-ivg"
