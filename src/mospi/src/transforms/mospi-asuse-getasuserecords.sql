-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: `frequency` mixes annual and quarterly observations in one table — filter on it before any time aggregation.
-- caution: Long-format indicator table: a dimension column is NULL when the row is not disaggregated along that dimension (the row is a total over it). Never aggregate `value` across rows without pinning every dimension column — totals and their components coexist.
SELECT
    "indicator",
    "frequency",
    "year",
    "state_UT" AS state_ut,
    "sector",
    "activity_category",
    "establishment_type",
    "value",
    "broad_activity_category",
    "ownership_type",
    "general_education_level",
    "social_group_of_owner_Major_partner" AS social_group_of_owner_major_partner,
    "other_economic_activitycount",
    "account_holder",
    "location_of_establishment",
    "nature_of_operation",
    "no_of_months_operated",
    "no_of_working_hours",
    "NPI_status" AS npi_status,
    "sub_indicator",
    "gender",
    "working_time",
    "type_of_worker",
    "hired_worker",
    "usage_of_internet",
    "worker_characteristics",
    "worker_number",
    "quarter"
FROM "mospi-asuse-getasuserecords"
