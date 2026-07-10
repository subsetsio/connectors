-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "minute_bucket",
    CAST("hits" AS BIGINT) AS hits
FROM "cdc-p5x4-u35c"
