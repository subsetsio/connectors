-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Long-format indicator table: a dimension column is NULL when the row is not disaggregated along that dimension (the row is a total over it). Never aggregate `value` across rows without pinning every dimension column — totals and their components coexist.
SELECT
    "indicator",
    "state",
    "type_of_goods",
    "sector",
    "value",
    "mobile_household_assets",
    "type_of_network",
    "major_reason",
    "agegroup",
    "gender",
    "mode_of_transaction",
    "mobile_type",
    "internet_access",
    "type_of_device_and_network",
    "level_of_enrollment",
    "expenditure_item",
    "type_of_school",
    "household_members",
    "sof"
FROM "mospi-nss80-getnss80records"
