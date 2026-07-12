-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are directional count observations by site, survey date, time interval, path, mode, and programme wave, but the raw source includes duplicate and blank-measurement rows; aggregate only after choosing the modes and directions relevant to the question.
SELECT
    "wave",
    "site_id",
    strptime("date", '%d/%m/%Y')::DATE AS date,
    "weather",
    "time",
    "day",
    "round",
    "direction",
    "path",
    "mode",
    CAST("count" AS BIGINT) AS count
FROM "transport-for-london-active-travel-counts"
