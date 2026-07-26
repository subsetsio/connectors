-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("year" AS BIGINT) AS year,
    "product",
    "product_label",
    "flow",
    "flow_label",
    "market_concentration_index",
    "market_concentration_index_footnote",
    "market_concentration_index_missing_value",
    "structural_change_index",
    "structural_change_index_footnote",
    "structural_change_index_missing_value"
FROM "unctad-us.biotrademerchmarketindices"
