-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: `category` carries the source's period or row label rather than a normalized date column.
SELECT
    "region",
    CAST("category" AS BIGINT) AS category,
    "metric",
    "value"
FROM "damodaran-macro"
