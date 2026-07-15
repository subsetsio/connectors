-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "quarter",
    "town",
    "flat_type",
    "price"
FROM "sg-data-d-b51323a474ba789fb4cc3db58a3116d4"
