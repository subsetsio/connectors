-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "state_abb",
    "state_name",
    "vote_date",
    "total_delegates",
    "allocated",
    "rules",
    "DeSantis" AS desantis,
    "Haley" AS haley,
    "Trump" AS trump,
    "model_date"
FROM "fivethirtyeight-gop-delegate-benchmarks-2024-previous-targets-delegate-targets-2024-01-19"
