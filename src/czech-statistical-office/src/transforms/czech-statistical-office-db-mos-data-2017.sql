-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("rok" AS BIGINT) AS rok,
    "kodukaz",
    CAST("koduzemi" AS BIGINT) AS koduzemi,
    "hodnota " AS hodnota
FROM "czech-statistical-office-db-mos-data-2017"
