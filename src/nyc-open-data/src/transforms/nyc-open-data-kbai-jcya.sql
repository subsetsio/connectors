-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_2005_category" AS 2005_category,
    "_2013_category" AS 2013_category,
    "_2017_category" AS 2017_category,
    "_2023_category" AS 2023_category,
    "comparative_category"
FROM "nyc-open-data-kbai-jcya"
