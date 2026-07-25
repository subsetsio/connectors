-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "MEASURES_" AS measures,
    CAST("Category_Parent" AS BIGINT) AS category_parent,
    "Oktmo_Parent" AS oktmo_parent,
    "Range_Sell_Code" AS range_sell_code,
    CAST("Range_Sell_Have" AS BIGINT) AS range_sell_have,
    CAST("time" AS BIGINT) AS time,
    "value"
FROM "rosstat-7708234640-vshp2016173"
