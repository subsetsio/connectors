-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "holc_city",
    "holc_state",
    "holc_grade",
    "holc_id",
    "holc_neighborhood_id",
    "block_geoid20",
    "pct_match"
FROM "fivethirtyeight-redlining-zone-block-matches"
