-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "1hr_pm25",
    "north",
    "south",
    "east",
    "west",
    "central"
FROM "sg-data-d-6c0d5fc34838b12472475fdb73c0af29"
