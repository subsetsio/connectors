-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ZKRATKA2" AS zkratka2,
    CAST("KODZEME" AS BIGINT) AS kodzeme,
    "NAZZEMECZ" AS nazzemecz,
    "NAZZEMEEN" AS nazzemeen,
    "NAZZKRCZ" AS nazzkrcz,
    "NAZZKREN" AS nazzkren,
    "ZKRATKA3" AS zkratka3
FROM "czech-statistical-office-ep2024czemeu"
