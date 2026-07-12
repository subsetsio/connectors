-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The source dump contains a rolling recent window, so this table reflects that recent window.
SELECT
    CAST("version_id" AS BIGINT) AS version_id,
    strptime("date", '%Y-%m-%d')::DATE AS date,
    CAST("downloads" AS BIGINT) AS downloads
FROM "crates-io-version-downloads-daily"
