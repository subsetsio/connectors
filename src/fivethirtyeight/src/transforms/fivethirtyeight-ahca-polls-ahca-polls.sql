-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Start" AS start,
    "End" AS end,
    "Pollster" AS pollster,
    "Favor" AS favor,
    "Oppose" AS oppose,
    "Url" AS url,
    "Text" AS text
FROM "fivethirtyeight-ahca-polls-ahca-polls"
