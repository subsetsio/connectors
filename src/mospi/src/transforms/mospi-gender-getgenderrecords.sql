-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: `year` mixes calendar years, fiscal-year labels and survey-round labels.
-- caution: `unit` varies by `indicator`; values are only comparable within one indicator.
-- caution: Long-format indicator table: a dimension column is NULL when the row is not disaggregated along that dimension (the row is a total over it). Never aggregate `value` across rows without pinning every dimension column — totals and their components coexist.
SELECT
    "year",
    "state_UT" AS state_ut,
    "indicator",
    "sector",
    "gender",
    "value",
    "unit",
    "age_group",
    "education_level",
    "birth_order_age_wise_" AS birth_order_age_wise,
    "sub_indicator",
    "survey",
    "family_planning_method",
    "category",
    "ayush_category",
    "discipline",
    "quarter",
    "NCO_division" AS nco_division,
    "employment_category",
    "industry",
    "activity",
    "bank_group",
    "deposit",
    "scheme",
    "broad_activity_category",
    "type_of_establishment",
    "lok_sabha_election",
    "court",
    "police",
    "service",
    "crime_head"
FROM "mospi-gender-getgenderrecords"
