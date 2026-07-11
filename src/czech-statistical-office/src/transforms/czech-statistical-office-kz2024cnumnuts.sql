-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("NUMNUTS" AS BIGINT) AS numnuts,
    "NUTS" AS nuts,
    "NAZEVNUTS" AS nazevnuts,
    CAST("KODCIS" AS BIGINT) AS kodcis,
    "CHODNOTA" AS chodnota
FROM "czech-statistical-office-kz2024cnumnuts"
