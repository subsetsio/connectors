-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "KODJAZ" AS kodjaz,
    "AKRCIS" AS akrcis,
    CAST("KODCIS" AS BIGINT) AS kodcis,
    CAST("UROVEN" AS BIGINT) AS uroven,
    "CHODNOTA" AS chodnota,
    "ZKRTEXT" AS zkrtext,
    "TEXT" AS text,
    strptime("ADMPLOD", '%Y-%m-%d')::DATE AS admplod,
    strptime("ADMNEPO", '%Y-%m-%d')::DATE AS admnepo,
    "NADVAZ" AS nadvaz
FROM "czech-statistical-office-cz-nace-res"
