-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "employment_size",
    "web_presence"
FROM "sg-data-d-f836f9bce300b89ebc7685ef9df1b822"
