-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "account_category",
    CAST("fy_2013" AS BIGINT) AS fy_2013,
    CAST("fy_2012" AS BIGINT) AS fy_2012
FROM "port-of-la-jdgw-bwcf"
