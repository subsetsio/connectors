-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are trailing-30-day summaries captured on a single date, not full historical time series observations.
SELECT
    "channel",
    "rank",
    "minutes_streamed",
    "avg_viewers",
    "max_viewers",
    "hours_watched",
    "followers",
    "followers_total",
    "captured_date"
FROM "twitch-tracker-channels"
