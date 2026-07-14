-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Steam Spy values are current estimates from a daily-refreshed public snapshot, not immutable historical observations.
SELECT
    "appid",
    "name",
    "developer",
    "publisher",
    "score_rank",
    "positive",
    "negative",
    "userscore",
    "owners",
    "average_forever",
    "average_2weeks",
    "median_forever",
    "median_2weeks",
    CAST("price" AS BIGINT) AS price,
    CAST("initialprice" AS BIGINT) AS initialprice,
    CAST("discount" AS BIGINT) AS discount,
    "ccu",
    "source_page"
FROM "steam-spy-apps"
