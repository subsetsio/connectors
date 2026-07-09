-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: `category` is NULL on the total rows that coexist with the per-category rows.
-- caution: Long-format indicator table: a dimension column is NULL when the row is not disaggregated along that dimension (the row is a total over it). Never aggregate `value` across rows without pinning every dimension column — totals and their components coexist.
SELECT
    "type_of_renewable_energy",
    CAST("year" AS BIGINT) AS year,
    "month",
    "state",
    "category",
    CAST("value" AS DOUBLE) AS value
FROM "mospi-mnre-getdatabyenergy"
