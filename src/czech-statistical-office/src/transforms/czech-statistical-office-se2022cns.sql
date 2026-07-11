-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("NSTRANA" AS BIGINT) AS nstrana,
    "NAZEV_STRN" AS nazev_strn,
    "ZKRATKAN30" AS zkratkan30,
    "ZKRATKAN8" AS zkratkan8
FROM "czech-statistical-office-se2022cns"
