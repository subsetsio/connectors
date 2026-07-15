-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "month",
    "level_1",
    "level_2",
    "value"
FROM "sg-data-d-75307bdff7cb61d0f8d79da552e8fe1d"
