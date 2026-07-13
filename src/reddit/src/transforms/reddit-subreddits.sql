-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is a current metadata snapshot for the connector's subreddit panel, not a historical dimension table.
SELECT
    "subreddit",
    "subscribers",
    CAST(to_timestamp("created_utc") AS TIMESTAMP) AS "created_at",
    "over18",
    "subreddit_type",
    "lang",
    "num_posts",
    "num_comments"
FROM "reddit-subreddits"
