-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "usa_or_hhsregion",
    CAST("week_ending" AS TIMESTAMP) AS week_ending,
    "variant",
    CAST("share" AS DOUBLE) AS share,
    CAST("share_hi" AS DOUBLE) AS share_hi,
    CAST("share_lo" AS DOUBLE) AS share_lo,
    "nchs_or_count_flag",
    "modeltype",
    "time_interval",
    CAST("published_date" AS TIMESTAMP) AS published_date
FROM "cdc-jr58-6ysp"
