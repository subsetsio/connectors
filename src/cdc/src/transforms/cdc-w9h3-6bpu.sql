-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "TOPIC" AS topic,
    "SUBTOPIC" AS subtopic,
    "DATA SHORTNAME" AS data_shortname,
    "CLASSIFICATION" AS classification,
    CAST("CLASSIFICATION_ID" AS BIGINT) AS classification_id,
    "FILTER" AS filter
FROM "cdc-w9h3-6bpu"
