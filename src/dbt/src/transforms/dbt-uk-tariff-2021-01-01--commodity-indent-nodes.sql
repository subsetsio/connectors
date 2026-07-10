-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("creating_transaction_id" AS BIGINT) AS creating_transaction_id,
    "path",
    CAST("indent_id" AS BIGINT) AS indent_id,
    CAST("numchild" AS BIGINT) AS numchild,
    CAST("depth" AS BIGINT) AS depth,
    "validity_start",
    "validity_end"
FROM "dbt-uk-tariff-2021-01-01--commodity-indent-nodes"
