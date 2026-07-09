-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Long-format indicator table: a dimension column is NULL when the row is not disaggregated along that dimension (the row is a total over it). Never aggregate `value` across rows without pinning every dimension column — totals and their components coexist.
SELECT
    "indicator",
    "state",
    "gender",
    "sector",
    CAST("value" AS DOUBLE) AS value,
    "arrangement_of_caregiver",
    "status_of_receipt_of_aid_help",
    "disability_type",
    "treatment_taken",
    "type_of_structure",
    "quintile_class",
    "sub_indicator",
    "dwelling_units",
    "tenurial_status",
    "distribution_by_experience_of_flood",
    "distribution_by_plinth_level",
    "principal_source_of_drinking_water",
    "method_of_treatment_of_water",
    "type_of_approach_road",
    "month",
    "agency_emptied",
    "households_percentage",
    "percentage_houses_number_floors_house",
    "percentage_houses_separate_kitchen",
    "material_category_type",
    "number_of_days",
    "types_of_latrine_uses"
FROM "mospi-nss76-getnss76records"
