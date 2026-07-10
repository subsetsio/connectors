-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "name",
    "year",
    "team",
    "league",
    "goose_eggs",
    "broken_eggs",
    "mehs",
    "league_average_gpct",
    "ppf",
    "replacement_gpct",
    "gwar",
    "key_retro"
FROM "fivethirtyeight-goose-goose-rawdata"
