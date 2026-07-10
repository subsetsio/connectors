-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Week Beginning" AS week_beginning,
    "Content Source URLs" AS content_source_urls,
    CAST("Page Views" AS BIGINT) AS page_views
FROM "cdc-rppv-wbiv"
