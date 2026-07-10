-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "stcd",
    "state",
    "cd",
    "pvi_22",
    "urbanindex",
    "rural",
    "exurban",
    "suburban",
    "urban",
    "grouping"
FROM "fivethirtyeight-district-urbanization-index-2022-urbanization-index-2022"
