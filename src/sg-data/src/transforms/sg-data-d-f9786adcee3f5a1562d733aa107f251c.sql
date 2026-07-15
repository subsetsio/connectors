-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "quarter",
    "level_1",
    "level_2",
    "level_3",
    "value"
FROM "sg-data-d-f9786adcee3f5a1562d733aa107f251c"
