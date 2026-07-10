-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "series",
    "date",
    CAST("division" AS BIGINT) AS division,
    "sales",
    "volume",
    "volume_sa"
FROM "dosm-iowrt-2d"
