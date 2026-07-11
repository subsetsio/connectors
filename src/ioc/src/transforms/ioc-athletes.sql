-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "edition",
    "games",
    "athlete_code",
    "source_url",
    CAST("archive_timestamp" AS BIGINT) AS archive_timestamp,
    "payload"
FROM "ioc-athletes"
