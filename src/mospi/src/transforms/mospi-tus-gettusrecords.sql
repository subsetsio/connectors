-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: `state` is a single all-India member; the table carries no state breakdown.
-- caution: `icatus_activity` totals coexist with individual ICATUS activities.
-- caution: Long-format indicator table: a dimension column is NULL when the row is not disaggregated along that dimension (the row is a total over it). Never aggregate `value` across rows without pinning every dimension column — totals and their components coexist.
SELECT
    CAST("year" AS BIGINT) AS year,
    "state",
    "indicator",
    "sector",
    "gender",
    "age_group",
    "icatus_activity",
    "day_of_week",
    "value",
    "unit",
    "activity",
    "usual_principal_activity",
    "marital_status",
    "quintile_class_of_umpce",
    "level_of_education",
    "social_group",
    "sub_indicator",
    "sna_activity",
    "broad_principal_activity_status",
    "place_of_activity"
FROM "mospi-tus-gettusrecords"
