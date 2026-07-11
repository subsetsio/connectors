-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Үзүүлэлт" AS column,
    CAST("Он" AS BIGINT) AS column_2,
    "value",
    "unit"
FROM "nso-mongolia-dt-nso-054v6-2"
