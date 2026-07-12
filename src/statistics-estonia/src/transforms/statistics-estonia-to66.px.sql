-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are not uniquely keyed by the exposed PxWeb label dimensions in the raw download; duplicate label-level combinations exist, so no table-level grain is asserted.
SELECT
    CAST("reference_period" AS BIGINT) AS reference_period,
    "product_ttl",
    "indicator",
    "value"
FROM "statistics-estonia-to66.px"
