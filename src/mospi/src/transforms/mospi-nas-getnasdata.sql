-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: `frequency` mixes annual and quarterly observations; quarterly rows carry `quarter`, annual rows leave it NULL.
-- caution: `revision` distinguishes the estimate vintage (provisional / revised); a year can appear more than once.
-- caution: Long-format indicator table: a dimension column is NULL when the row is not disaggregated along that dimension (the row is a total over it). Never aggregate `value` across rows without pinning every dimension column — totals and their components coexist.
SELECT
    "base_year",
    "series",
    "year",
    "indicator",
    "frequency",
    "revision",
    "industry",
    "subindustry",
    "institutional_sector",
    "quarter",
    CAST("current_price" AS DOUBLE) AS current_price,
    "constant_price",
    "unit"
FROM "mospi-nas-getnasdata"
