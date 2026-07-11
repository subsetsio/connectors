-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("kod" AS BIGINT) AS kod,
    "text",
    "text_en",
    strptime("platiod", '%Y-%m-%d')::DATE AS platiod,
    strptime("neplatipo", '%Y-%m-%d')::DATE AS neplatipo,
    "definice",
    "definice_en"
FROM "czech-statistical-office-990124-17"
