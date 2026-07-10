-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "created_at",
    "emojis",
    "id",
    "link",
    "retweeted",
    "screen_name",
    "text"
FROM "fivethirtyeight-mayweather-mcgregor-tweets"
