-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "month",
    "level_1",
    "level_2",
    "total_loans"
FROM "sg-data-d-c2e116320c9d36f6ea6cdd82fb763de2"
