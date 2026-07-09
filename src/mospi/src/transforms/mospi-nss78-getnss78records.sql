-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Long-format indicator table: a dimension column is NULL when the row is not disaggregated along that dimension (the row is a total over it). Never aggregate `value` across rows without pinning every dimension column — totals and their components coexist.
SELECT
    "state",
    "age_group",
    "sector",
    "gender",
    "indicator",
    "sub_indicator",
    "internet_access",
    "household",
    "source_of_finance",
    "main_reason_for_migration",
    "value"
FROM "mospi-nss78-getnss78records"
