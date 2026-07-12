-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "description",
    "industry",
    CAST("level" AS BIGINT) AS level,
    "size",
    "line_code",
    CAST("value" AS BIGINT) AS value
FROM "statsnz-business-operations-survey-2022-business-finance"
