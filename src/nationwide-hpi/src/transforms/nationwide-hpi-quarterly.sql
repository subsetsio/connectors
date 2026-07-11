-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This table is the UK quarterly series; use regional quarterly tables for regional comparisons.
SELECT
    "date",
    "period_label",
    "category",
    "measure",
    "value"
FROM "nationwide-hpi-quarterly"
