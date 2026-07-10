-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "C0" AS c0,
    "name",
    "newPerct2013" AS newperct2013
FROM "fivethirtyeight-most-common-name-new-top-firstnames"
