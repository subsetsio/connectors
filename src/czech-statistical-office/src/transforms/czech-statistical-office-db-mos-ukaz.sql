-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "kodukaz",
    "nazev",
    "mj",
    CAST("platiod" AS BIGINT) AS platiod,
    CAST("platido" AS BIGINT) AS platido,
    "okruh",
    "zdroj",
    "verifikace_csu",
    "metodika " AS metodika
FROM "czech-statistical-office-db-mos-ukaz"
