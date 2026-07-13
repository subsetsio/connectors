-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are long-form metric observations by subreddit; pivot or filter `metric` before aggregating activity values.
-- caution: The subreddit panel is limited to communities above the connector's current subscriber threshold, so it is not an all-subreddit census.
SELECT
    "subreddit",
    "metric",
    CAST(to_timestamp("date") AS TIMESTAMP) AS "period_start",
    "value"
FROM "reddit-subreddit-activity"
