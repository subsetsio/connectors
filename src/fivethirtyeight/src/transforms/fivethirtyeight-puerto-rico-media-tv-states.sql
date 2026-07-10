-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Date" AS date,
    "Florida" AS florida,
    "Texas" AS texas,
    "Puerto Rico" AS puerto_rico
FROM "fivethirtyeight-puerto-rico-media-tv-states"
