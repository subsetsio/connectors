-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "local",
    "foreign",
    "total"
FROM "sg-data-d-314ec79776cf210a7489e1399213df5d"
