-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Date" AS date,
    "Query" AS query,
    "BBC News" AS bbc_news,
    "CNN" AS cnn,
    "FOX News" AS fox_news,
    "MSNBC" AS msnbc
FROM "fivethirtyeight-puerto-rico-media-tv-hurricanes-by-network"
