-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The subreddit panel is limited to communities above the connector's current subscriber threshold, so it is not an all-subreddit census.
SELECT
    "subreddit",
    CAST(to_timestamp("date") AS TIMESTAMP) AS "period_start",
    "value" AS "subscribers"
FROM "reddit-subreddit-subscribers"
