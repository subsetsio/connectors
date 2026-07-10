-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "country",
    "country_id",
    "group",
    "spi",
    "spi_offense",
    "spi_defense",
    "win_group",
    "sixteen",
    "quarter",
    "semi",
    "cup",
    "win"
FROM "fivethirtyeight-world-cup-predictions-wc-20140618-175722"
