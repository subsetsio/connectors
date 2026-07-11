-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("OBEC_PREZ" AS BIGINT) AS obec_prez,
    "NAZEVOBCE" AS nazevobce
FROM "czech-statistical-office-se2024cisob"
