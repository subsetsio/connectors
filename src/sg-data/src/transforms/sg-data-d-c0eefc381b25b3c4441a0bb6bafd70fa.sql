-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "quarter",
    "industry",
    "gross_allocation",
    "returns"
FROM "sg-data-d-c0eefc381b25b3c4441a0bb6bafd70fa"
