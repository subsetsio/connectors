-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "accounts_category",
    CAST("as_of_march_2014" AS BIGINT) AS as_of_march_2014,
    CAST("as_of_march_2013" AS BIGINT) AS as_of_march_2013
FROM "port-of-la-v7gk-cxxi"
