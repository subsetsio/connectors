-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Topic" AS topic,
    "Question" AS question,
    "VariableName" AS variablename,
    "Responses" AS responses,
    CAST("Year" AS BIGINT) AS year,
    "Type" AS type,
    CAST("DisplayOrder" AS BIGINT) AS displayorder
FROM "cdc-iuq5-y9ct"
