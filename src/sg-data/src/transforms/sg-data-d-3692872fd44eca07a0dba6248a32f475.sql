-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "level_1",
    "level_2",
    "value"
FROM "sg-data-d-3692872fd44eca07a0dba6248a32f475"
