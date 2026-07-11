-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("VOLKRAJ" AS BIGINT) AS volkraj,
    "NAZVOLKRAJ" AS nazvolkraj,
    CAST("KRAJ" AS BIGINT) AS kraj,
    CAST("MAXKAND" AS BIGINT) AS maxkand
FROM "czech-statistical-office-ps2021cvolkr"
