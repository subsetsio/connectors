-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "unique_carrier_name",
    CAST("full_time_employees" AS BIGINT) AS full_time_employees,
    CAST("part_time_employees" AS BIGINT) AS part_time_employees,
    CAST("total_employees" AS BIGINT) AS total_employees,
    CAST("full_time_equivalent_employees" AS BIGINT) AS full_time_equivalent_employees
FROM "u-s-department-of-transportation-em9t-xx9j"
