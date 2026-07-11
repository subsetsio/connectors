-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("KRZAST" AS BIGINT) AS krzast,
    "NAZEVKRZ" AS nazevkrz,
    CAST("MANDATYKRZ" AS BIGINT) AS mandatykrz,
    CAST("KRAJ" AS BIGINT) AS kraj
FROM "czech-statistical-office-kz2024ciskr"
