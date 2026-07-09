-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Two base-year series coexist: the 2011-12 series uses `base_year`/`major_group`/`sub_group`/`sub_sub_group`, the older series uses `majorgroup`/`group`/`subgroup`/`sub_subgroup`. Exactly one set is populated per row.
-- caution: `item` is NULL on group-level rows — group totals and their items coexist.
-- caution: Long-format indicator table: a dimension column is NULL when the row is not disaggregated along that dimension (the row is a total over it). Never aggregate `value` across rows without pinning every dimension column — totals and their components coexist.
SELECT
    CAST("year" AS BIGINT) AS year,
    "month",
    "majorgroup",
    "group",
    "subgroup",
    "sub_subgroup",
    "item",
    CAST("index_value" AS DOUBLE) AS index_value,
    "base_year",
    "major_group",
    "sub_group",
    "sub_sub_group"
FROM "mospi-wpi-getwpirecords"
