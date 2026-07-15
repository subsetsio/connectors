-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "age",
    "activity",
    "sample",
    "hours"
FROM "sg-data-d-5ead501e7ac28f12c1655499bfd4b223"
