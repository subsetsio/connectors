-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: `frequency` mixes annual, quarterly and monthly observations in one table.
-- caution: Annual rows carry `year_type` ('July-June'); quarterly rows carry `quarter`.
-- caution: Long-format indicator table: a dimension column is NULL when the row is not disaggregated along that dimension (the row is a total over it). Never aggregate `value` across rows without pinning every dimension column — totals and their components coexist.
SELECT
    "year_type",
    CAST("year" AS BIGINT) AS year,
    "frequency",
    "indicator",
    "state",
    "gender",
    "sector",
    "AgeGroup" AS agegroup,
    "weekly_status",
    "religion",
    "socialGroup" AS socialgroup,
    "General_Education" AS general_education,
    "quarter",
    "month",
    "employee_contract",
    "value",
    "unit",
    "broad_industry_work",
    "broad_status_employment",
    "enterprise_type",
    "industry_section",
    "nco_division",
    "nic_group"
FROM "mospi-plfs-getdata"
