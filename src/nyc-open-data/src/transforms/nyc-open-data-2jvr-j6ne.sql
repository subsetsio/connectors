-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "element",
    "recommended",
    "present",
    "damaged",
    "_comments" AS comments,
    "outstanding",
    "inspection_id",
    "element_id",
    CAST("nowatercount" AS BIGINT) AS nowatercount
FROM "nyc-open-data-2jvr-j6ne"
