-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: `year` is a fiscal school year (e.g. '2021-22').
-- caution: Long-format indicator table: a dimension column is NULL when the row is not disaggregated along that dimension (the row is a total over it). Never aggregate `value` across rows without pinning every dimension column — totals and their components coexist.
SELECT
    "indicator",
    "year",
    "state",
    "value",
    "level_of_education",
    "enrolement_bracket",
    "social_group",
    "infrastructure_facility",
    "type_of_management",
    "category",
    "gender",
    "class_taught",
    "sub_indicator",
    "age_group",
    "source_of_drinking_water",
    "facility_of_labs"
FROM "mospi-udise-getudiserecords"
