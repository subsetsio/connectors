-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "quarter",
    "level_1",
    "level_2",
    "value"
FROM "sg-data-d-ffe9af32e8fdd8bd77acd6fa97ef74a7"
