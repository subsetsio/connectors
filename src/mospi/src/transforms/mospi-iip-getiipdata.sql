-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows with a NULL `month` are annual (fiscal-year) figures; rows with a month are monthly. Filter on `month IS NULL` to separate them.
-- caution: Four base-year series (`base_year`) coexist and their index levels are not comparable.
-- caution: Long-format indicator table: a dimension column is NULL when the row is not disaggregated along that dimension (the row is a total over it). Never aggregate `value` across rows without pinning every dimension column — totals and their components coexist.
SELECT
    "base_year",
    "year",
    "type",
    "category",
    "sub_category",
    CAST("index" AS DOUBLE) AS index,
    CAST("growth_rate" AS DOUBLE) AS growth_rate,
    "month"
FROM "mospi-iip-getiipdata"
