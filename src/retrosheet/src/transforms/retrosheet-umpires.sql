-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id",
    "lastname",
    "firstname",
    CAST("first_g" AS BIGINT) AS first_g,
    CAST("last_g" AS BIGINT) AS last_g
FROM "retrosheet-umpires"
