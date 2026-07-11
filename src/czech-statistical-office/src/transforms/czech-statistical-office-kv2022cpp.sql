-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("PSTRANA" AS BIGINT) AS pstrana,
    "NAZEV_STRP" AS nazev_strp,
    "ZKRATKAP30" AS zkratkap30,
    "ZKRATKAP8" AS zkratkap8
FROM "czech-statistical-office-kv2022cpp"
